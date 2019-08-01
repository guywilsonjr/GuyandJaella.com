#!/usr/bin/env python3
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_assets as assets,
    aws_s3_deployment as deployments,
    aws_cloudfront as cf

)
from function_stack import FunctionStack
from aws_cdk.aws_s3_deployment import Source


class Website(core.Stack):

    def __init__(
            self,
            app: core.App,
            id: str,
            domain: str) -> None:
        super().__init__(app, id)
        rule = s3.CorsRule(
            allowed_methods=[
                s3.HttpMethods.GET],
            allowed_origins=['*'])
        site_bucket = s3.Bucket(
            self,
            '{}SiteBucket'.format(id),
            website_error_document='README.md',
            website_index_document='dashboard.html',
            public_read_access=True,
            removal_policy=core.RemovalPolicy.DESTROY,
            cors=[rule]
        )
        deployment_source = Source.asset('site/')
        deployments.BucketDeployment(
            self,
            '{}BucketDeployment'.format(id),
            destination_bucket=site_bucket,
            source=deployment_source,
            retain_on_delete=False)

        site_identity = cf.CfnCloudFrontOriginAccessIdentity(
            self,
            'SiteCFIdentity'.format(id),
            cloud_front_origin_access_identity_config=cf.CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty(
                comment='Website Origin Identity'))

        origin = cf.S3OriginConfig(
            s3_bucket_source=site_bucket,
            origin_access_identity_id=site_identity.ref
        )

        cf.CloudFrontWebDistribution(
            self,
            '{}SiteDistribution'.format(id),

            origin_configs=[
                cf.SourceConfiguration(
                    s3_origin_source=origin,
                    behaviors=[
                        cf.Behavior(
                            allowed_methods=cf.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                            is_default_behavior=True,
                            # TODO
                            # https://github.com/guywilsonjr/GuyandJaella.com/issues/1
                            compress=False,
                            default_ttl=core.Duration.seconds(
                                30),

                        )])],
            logging_config=cf.LoggingConfiguration(include_cookies=True))
