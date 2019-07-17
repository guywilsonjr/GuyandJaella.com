#!/usr/bin/env python3
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_assets as assets,
    aws_cloudfront as cf

)
from function_stack import FunctionStack


class WebsiteStack(core.Stack):

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
        site_identity = cf.CfnCloudFrontOriginAccessIdentity(
            self,
            'SiteCFIdentity'.format(id),
            cloud_front_origin_access_identity_config=cf.CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty(
                comment='Website Origin Identity'))
        s3_origin = cf.S3OriginConfig(
            s3_bucket_source=site_bucket.bucket_name,
            origin_access_identity_id=site_identity.attr_s3_canonical_user_id
        )
