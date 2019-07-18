#!/usr/bin/env python3
from aws_cdk import core, aws_certificatemanager as cm, aws_route53 as r53, aws_iam as iam, aws_lambda as lamb
import boto3


basic_acm_permissions = [
    'acm:ListCertificates',
    'acm:RequestCertificate',
    'acm:DescribeCertificate'
]


class FunctionStack(core.Stack):

    def set_minimal_policy(self, role):
        iam.Policy(self, 'MinimalFunctionPolicyDocument', roles=[
                   role], statements=self.get_minimal_policy_statements())

    def get_minimal_actions(self):
        return ['xray:PutTraceSegments',
                'xray:PutTelemetryRecords',
                'logs:CreateLogGroup',
                'logs:CreateLogStream',
                'logs:DescribeLogGroups',
                'logs:DescribeLogStreams',
                'logs:PutLogEvents',
                'logs:GetLogEvents',
                'logs:FilterLogEvents',
                'acm:ListCertificates',
                'acm:RequestCertificate',
                'acm:DescribeCertificate',
                's3:PutObject',
                'route53:ChangeResourceRecordSets'
                ]

    def get_minimal_policy_statements(self):
        return [
            iam.PolicyStatement(
                actions=self.get_minimal_actions(),
                resources=['*'])]

    def __init__(self,
                 app: core.App,
                 id: str,
                 seconds: core.Duration,
                 code_file_name: str,
                 handler: str,
                 env: dict,
                 timeout_seconds: int) -> None:

        super().__init__(app, id)
        role = iam.Role(
            self,
            '{}FunctionRole'.format(id),
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'))
        self.set_minimal_policy(role)
        code_txt = None
        with open(code_file_name, "r") as content:
            code_txt = content.read()
        function = lamb.Function(
            self,
            '{}Function'.format(id),
            timeout=core.Duration.seconds(timeout_seconds),
            code=lamb.Code.inline(code_txt),
            runtime=lamb.Runtime(
                'python3.7',
                supports_inline_code=True,
                handler=handler,
                environment=env,
                tracing=lamb.Tracing.ACTIVE,
                role=role
            )
        )

        self.name = function.function_name
        self.arn = function.function_arn
