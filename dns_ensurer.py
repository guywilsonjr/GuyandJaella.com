from aws_cdk.core import App, Stack
from aws_cdk.aws_lambda import SingletonFunction, Runtime, Tracing, Code
from aws_cdk.aws_events_targets import LambdaFunction
from aws_cdk.aws_iam import Policy, PolicyStatement
from aws_cdk.aws_events import Schedule, Rule
from aws_cdk.aws_route53 import HostedZone
from datetime import datetime, timedelta
from uuid import uuid4

class DnsEnsurer(Stack):
    '''
    This is a thin wrapper around a lambda function to create it in a separate stack
    '''

    def __init__(
            self,
            app: App,
            id: str,
            txt: str,
            env: dict,
            policies: PolicyStatement,
            domain: str) -> None:
        super().__init__(app, id)

        self.zone = HostedZone(
            self,
            'HostedZone{}'.format(domain),
            zone_name=domain)
        env['HOSTED_ZONE_ID'] = self.zone.hosted_zone_id

        self.function = SingletonFunction(
            self,
            '{}Function'.format('{}'.format(id)),
            uuid=str(uuid4()),
            code=Code.inline(txt),
            runtime=Runtime('python3.7', supports_inline_code=True),
            handler='index.handler',
            environment=env
        )

        policy = Policy(self, '{}Policy'.format(id))
        self.function.role.attach_inline_policy(policy)
        policy.add_statements(policies)
        rule_target = LambdaFunction(self.function)

        current_time = datetime.now()
        run_time = current_time + timedelta(minutes=3)
        run_schedule = Schedule.cron(
            year=str(run_time.year),
            month=str(run_time.month),
            day=str(run_time.day),
            hour=str(run_time.hour),
            minute=str(run_time.minute))

        self.rule = Rule(
            self,
            '{}Rule'.format(id),
            enabled=True,
            schedule=run_schedule,
            targets=[rule_target])
