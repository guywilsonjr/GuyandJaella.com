from asyncio import run, create_task
from aws_cdk.core import Duration, App, Stack, RemovalPolicy
from aws_cdk.aws_s3_deployment import Source, BucketDeployment
from aws_cdk.aws_lambda import Function, S3Code, Runtime, Tracing, InlineCode
from aws_cdk.aws_apigateway import LambdaRestApi, RestApi, LambdaIntegration, EndpointType, AuthorizationType, DomainNameOptions
from aws_cdk.aws_iam import ServicePrincipal, Role
from aws_cdk.aws_cloudfront import CloudFrontWebDistribution, CloudFrontAllowedMethods, Behavior, LoggingConfiguration, CfnCloudFrontOriginAccessIdentity, S3OriginConfig, SourceConfiguration
from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods
from aws_cdk.aws_s3_assets import Asset
from aws_cdk.aws_certificatemanager import Certificate
from aws_cdk.aws_route53 import ARecord, RecordTarget, HostedZone
from aws_cdk.aws_route53_targets import ApiGateway
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import LambdaFunction
from site_function.site_function import METRICS
from permissions import MINIMAL_FUNCTION_POLICY_STATEMENT, MINIMAL_PUBLIC_API_POLICY_DOCUMENT, DDB_FUNCTION_POLICY_STATEMENT
from app_metrics import AppMetrics
from api_custom_domain import APICustomDomain


class Website(Stack):
    api_resources = {
        'Snakes': ['GET', 'POST'],
        'Home': ['GET'],
        'Dashboard': ['GET'],
        'Snake': ['GET']
    }

    API_CHILD_RESOURCES = {'Snake': 'New'}

    def __init__(
            self,
            app: App,
            id: str,
            domain: str) -> None:
        super().__init__(app, id)
        run(self.setup(id=id, domain=domain))

    async def setup(self, id:str, domain: str) -> None:
        bucket_task = create_task(self.create_site_bucket(id=id))
        canary_task = create_task(self.create_canary_function(id=id))
        
        self.metrics = AppMetrics(self, '{}Metrics'.format(id), app_name=domain, metrics=METRICS)
    
        logging_bucket = Bucket(self, '{}DistroLogBucket'.format(
            id), removal_policy=RemovalPolicy.DESTROY)
        
        log_config = LoggingConfiguration(
            bucket=logging_bucket, include_cookies=True)
        site_identity = CfnCloudFrontOriginAccessIdentity(
            self,
            '{}SiteCFIdentity'.format(
                id),
            cloud_front_origin_access_identity_config=CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty(
                comment='Website Origin Identity'))
        
        self.site_bucket = await bucket_task
        origin = S3OriginConfig(
            s3_bucket_source=self.site_bucket,
            origin_access_identity_id=site_identity.ref
        )
        '''
        self.distribution = CloudFrontWebDistribution(
            self,
            '{}SiteDistribution'.format(id),
            default_root_object='template.html',
            origin_configs=[
                SourceConfiguration(
                    s3_origin_source=origin,
                    behaviors=[
                        Behavior(
                            allowed_methods=CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                            is_default_behavior=True,
                            compress=True,
                            default_ttl=Duration.seconds(30),
                        )])],
            logging_config=log_config)
        cdn_name = self.distribution.domain_name
        '''
        cdn_name = domain
        self.site_function = await self.create_site_function(id=id, domain=domain, cdn_name=cdn_name)
        self.acd = APICustomDomain(
            self, '{}APICustomDomain'.format(id), domain=domain, sats=['guyandjaella.com', '*.guyandjaella.com'])
        await self.acd.setup(domain=domain, sats=['guyandjaella.com', '*.guyandjaella.com'])
        self.api = LambdaRestApi(
            self,
            '{}API'.format(id),
            domain_name=self.acd.dno,
            handler=self.site_function,
            proxy=False,
            endpoint_types=[
                EndpointType.EDGE],
            cloud_watch_role=False,
            policy=MINIMAL_PUBLIC_API_POLICY_DOCUMENT,
            deploy=True,
            default_method_options={
                'authorizationType': AuthorizationType.NONE})

        self.api.root.add_method(
            http_method='GET',
            integration=LambdaIntegration(self.site_function),
            authorization_type=AuthorizationType.NONE)
        for resource, methods in self.api_resources.items():
            res = self.api.root.add_resource(resource)
            for method in methods:
                if resource in self.API_CHILD_RESOURCES:
                    child_res = res.add_resource(
                        self.API_CHILD_RESOURCES[resource])
                    child_res.add_method(
                        http_method=method,
                        integration=LambdaIntegration(self.site_function),
                        authorization_type=AuthorizationType.NONE)

                method = res.add_method(
                    http_method=method,
                    integration=LambdaIntegration(self.site_function),
                    authorization_type=AuthorizationType.NONE)
                   
        
        target = ApiGateway(self.api)
        self.dns_record = ARecord(
            self,
            '{}DNSRecord'.format(id),
            target=RecordTarget(alias_target=target),
            zone=self.acd.zone,
            record_name='www.{}'.format(domain))
            
        self.canary_function = await canary_task
        Rule(self,
             '{}CanaryRule'.format(id),
             enabled=True,
             schedule=Schedule.cron(),
             targets=[LambdaFunction(handler=self.canary_function)])
             
    async def create_site_bucket(self, id: str) -> Bucket:
        cors_rule = CorsRule(
            allowed_methods=[
                HttpMethods.GET],
            allowed_origins=['*'])

        bucket = Bucket(
            self,
            '{}StaticBucket'.format(id),
            website_error_document='README.md',
            website_index_document='template.html',
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            cors=[cors_rule]
        )
        deployment_source = Source.asset('site/')
        BucketDeployment(
            self,
            '{}StaticDeployment'.format(id),
            destination_bucket=bucket,
            source=deployment_source,
            retain_on_delete=False)
        return bucket
        
    async def create_site_function(self, id: str, domain: str, cdn_name: str) -> Function:
        env = {
            'PROD': 'True',
            'SITE_DOMAIN': domain,
            'APP_VERSION': '0.01',
            'STATIC_DOMAIN': cdn_name
        }
        site_code_asset = Asset(
            self,
            '{}FunctionAsset'.format(id),
            path='site_function')
        site_code = S3Code(
            bucket=site_code_asset.bucket,
            key=site_code_asset.s3_object_key)
        return Function(
            self,
            '{}Function'.format(id),
            timeout=Duration.seconds(3),
            code=site_code,
            handler='site_function.handler',
            environment=env,
            tracing=Tracing.ACTIVE,
            initial_policy=[DDB_FUNCTION_POLICY_STATEMENT],
            runtime=Runtime(
                name='python3.7',
                supports_inline_code=True,
            )
        )
    
    async def create_canary_function(self, id: str) -> Function:
        with open('canary/canary.py', 'r') as code:
            canary_code = code.read()
            return Function(
                self,
                '{}CanaryFunction'.format(id),
                timeout=Duration.seconds(3),
                code=InlineCode(canary_code),
                handler='canary.handler',
                tracing=Tracing.ACTIVE,
                initial_policy=[MINIMAL_FUNCTION_POLICY_STATEMENT],
                runtime=Runtime(
                    name='python3.7',
                    supports_inline_code=True,
                )
            )

    
