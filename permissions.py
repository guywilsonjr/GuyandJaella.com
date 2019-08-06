from aws_cdk import aws_iam as iam

MINIMAL_FUNCTION_ACTIONS = ['xray:PutTraceSegments',
                            'xray:PutTelemetryRecords',
                            'logs:CreateLogGroup',
                            'logs:CreateLogStream',
                            'logs:DescribeLogGroups',
                            'logs:DescribeLogStreams',
                            'logs:PutLogEvents',
                            'logs:GetLogEvents',
                            'logs:FilterLogEvents'
                            ]
DDB_ACTIONS = ['dynamodb:Scan', 'dynamodb:PutItem']
API_INVOKE_STATEMENT_ACTION = 'execute-api:Invoke'


MINIMAL_FUNCTION_POLICY_STATEMENT = iam.PolicyStatement(
    actions=MINIMAL_FUNCTION_ACTIONS, resources=['*'])

MINIMAL_API_POLICY_STATEMENT = iam.PolicyStatement(
    actions=MINIMAL_FUNCTION_ACTIONS,
    resources=['*'],
    principals=[iam.ServicePrincipal('apigateway.amazonaws.com')])

PUBLIC_INVOKE_POLICY_STATEMENT = iam.PolicyStatement(
    actions=[API_INVOKE_STATEMENT_ACTION],
    resources=['*'],
    principals=[iam.Anyone()])


MINIMAL_PUBLIC_API_POLICY_DOCUMENT = iam.PolicyDocument(
    statements=[
        MINIMAL_API_POLICY_STATEMENT,
        PUBLIC_INVOKE_POLICY_STATEMENT])


def get_ddb_function_statement(table_arns):
    return iam.PolicyStatement(
        actions=MINIMAL_FUNCTION_ACTIONS + DDB_ACTIONS,
        resources=table_arns)
