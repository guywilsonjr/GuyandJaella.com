#!/usr/bin/env python3
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_assets as assets,
    aws_s3_deployment as deployments,
    aws_cloudfront as cf
)
from permissions import MINIMAL_FUNCTION_POLICY_STATEMENT, MINIMAL_PUBLIC_API_POLICY_DOCUMENT
from aws_cdk.aws_s3_deployment import Source
from aws_cdk.aws_lambda import Function, Code, Runtime, Tracing
from aws_cdk.aws_apigateway import LambdaRestApi, LambdaIntegration, EndpointType, AuthorizationType
from aws_cdk.aws_iam import ServicePrincipal, Role
from aws_cdk.aws_cloudfront import CloudFrontWebDistribution, CloudFrontAllowedMethods, Behavior, LoggingConfiguration, CfnCloudFrontOriginAccessIdentity, S3OriginConfig, SourceConfiguration
from aws_cdk.aws_s3 import Bucket


class Website(core.Stack):
    api_resources = {
        'Snakes': ['GET']
    }

    def __init__(
            self,
            app: core.App,
            id: str,
            domain: str, cert_arn: str) -> None:
        super().__init__(app, id)
        site_bucket = self.setup_site_bucket()
        distribution = self.create_s3_distirbution(site_bucket)
        lambda_env = {'STATIC_DOMAIN': distribution.domain_name}

        function = self.create_lambda(
            code_file='function/site_function.py',
            handler='index.handler',
            runtime='python3.7',
            env=lambda_env,
            timeout=3)

        self.create_api(
            function=function,
            domain=domain,
            resources=api_resources)

    def setup_site_bucket(self) -> Bucket:
        # TODO use more restrictive rule
        # https://github.com/guywilsonjr/GuyandJaella.com/issues/8
        rule = s3.CorsRule(
            allowed_methods=[
                s3.HttpMethods.GET],
            allowed_origins=['*'])
        site_bucket = Bucket(
            self,
            '{}StaticBucket'.format(id),
            website_error_document='README.md',
            website_index_document='dashboard.html',
            public_read_access=True,
            removal_policy=core.RemovalPolicy.DESTROY,
            cors=[rule]
        )
        deployment_source = Source.asset('site/')
        deployments.BucketDeployment(
            self,
            '{}StaticDeployment'.format(id),
            destination_bucket=site_bucket,
            source=deployment_source,
            retain_on_delete=False)
        return site_bucket

    def create_s3_distirbution(
            self,
            site_bucket: Bucket) -> CloudFrontWebDistribution:

        logging_bucket = Bucket(self, '{}DistroLogBucket'.format(
            id), removal_policy=core.RemovalPolicy.DESTROY)

        log_config = LoggingConfiguration(
            bucket=logging_bucket, include_cookies=True)
        site_identity = CfnCloudFrontOriginAccessIdentity(
            self,
            'SiteCFIdentity'.format(id),
            cloud_front_origin_access_identity_config=CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty(
                comment='Website Origin Identity'))

        origin = S3OriginConfig(
            s3_bucket_source=site_bucket,
            origin_access_identity_id=site_identity.ref
        )

        return CloudFrontWebDistribution(
            self,
            '{}SiteDistribution'.format(id),

            origin_configs=[
                SourceConfiguration(
                    s3_origin_source=origin,
                    behaviors=[
                        Behavior(
                            allowed_methods=CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                            is_default_behavior=True,
                            # TODO
                            # https://github.com/guywilsonjr/GuyandJaella.com/issues/1
                            compress=True,
                            default_ttl=core.Duration.seconds(
                                30),

                        )])],
            logging_config=log_config)

    def create_lambda(
            self,
            code_file: str,
            handler: str,
            runtime: str,
            env: dict,
            timeout: int) -> None:

        role = Role(
            self,
            '{}FunctionRole'.format(id),
            assumed_by=ServicePrincipal('lambda.amazonaws.com'))

        return Function(
            self,
            '{}Function'.format(id),
            timeout=core.Duration.seconds(timeout),
            code=Code.inline('function/site_function.py'),
            handler='index.handler',
            environment=env,
            tracing=Tracing.ACTIVE,
            initial_policy=[MINIMAL_FUNCTION_POLICY_STATEMENT],
            runtime=Runtime(
                name='python3.7',
                supports_inline_code=True,
            ),
            role=role
        )

    def create_api(
            self,
            function: Function,
            resources: dict,
            domain: str) -> None:

        api = LambdaRestApi(
            self,
            '{}API'.format(id),
            handler=function,
            proxy=False,
            endpoint_types=[
                EndpointType.EDGE],
            cloud_watch_role=False,
            policy=MINIMAL_PUBLIC_API_POLICY_DOCUMENT,
            deploy=True,
            default_method_options={
                'authorizationType': AuthorizationType.NONE})

        for resource, methods in self.api_resources.items():
            res = api.root.add_resource(resource)
            for method in methods:
                method = res.add_method(
                    http_method=method,
                    integration=LambdaIntegration(function),
                    authorization_type=AuthorizationType.NONE)
