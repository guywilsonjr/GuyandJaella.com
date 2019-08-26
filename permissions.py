from aws_cdk.aws_iam import PolicyStatement, ServicePrincipal, Anyone, PolicyDocument

MINIMAL_FUNCTION_ACTIONS = ['xray:PutTraceSegments',
                            'xray:PutTelemetryRecords',
                            'logs:CreateLogGroup',
                            'logs:CreateLogStream',
                            'logs:DescribeLogGroups',
                            'logs:DescribeLogStreams',
                            'logs:PutLogEvents',
                            'logs:GetLogEvents',
                            'logs:FilterLogEvents',
                            'cloudwatch:PutMetricData'
                            ]
DDB_ACTIONS = ['dynamodb:Scan', 'dynamodb:PutItem']
API_INVOKE_STATEMENT_ACTION = 'execute-api:Invoke'

ROUTE_53_DNS_ENSURER_ACTIONS = [
    'route53domains:GetDomainDetail',
    'route53domains:UpdateDomainNameservers',
    'route53:GetHostedZone']

ROUTE_53_DNS_ENSURER_POLICY_STATEMENT = PolicyStatement(
    actions=MINIMAL_FUNCTION_ACTIONS + ROUTE_53_DNS_ENSURER_ACTIONS,
    resources=['*'])

MINIMAL_FUNCTION_POLICY_STATEMENT = PolicyStatement(
    actions=MINIMAL_FUNCTION_ACTIONS, resources=['*'])

MINIMAL_API_POLICY_STATEMENT = PolicyStatement(
    actions=MINIMAL_FUNCTION_ACTIONS,
    resources=['*'],
    principals=[ServicePrincipal('apigateway.amazonaws.com')])

PUBLIC_INVOKE_POLICY_STATEMENT = PolicyStatement(
    actions=[API_INVOKE_STATEMENT_ACTION],
    resources=['*'],
    principals=[Anyone()])


MINIMAL_PUBLIC_API_POLICY_DOCUMENT = PolicyDocument(
    statements=[
        MINIMAL_API_POLICY_STATEMENT,
        PUBLIC_INVOKE_POLICY_STATEMENT])


DDB_FUNCTION_POLICY_STATEMENT = PolicyStatement(
        actions=MINIMAL_FUNCTION_ACTIONS + DDB_ACTIONS,
        resources=['*'])
