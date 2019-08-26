import os
from aws_cdk.core import App, Stack, Duration
from aws_cdk.aws_cloudwatch import Metric, Unit
from site_function.site_function import METRICS


class AppMetrics(Stack):
    def __init__(
            self,
            app: App,
            id: str,
            app_name: str,
            metrics: list) -> None:
        super().__init__(app, id)
        stage = 'DEV'
        if 'PROD' in os.environ:
            stage = 'PROD'
        else:
            stage = 'DEV'

        for metric in metrics:
            operation = metric[0]
            metric_type = metric[1]
            color = metric[2]

            dim = {
                'By App Version': '0.01',
                'By Operation': operation,
                'By Stage': stage}

            Metric(metric_name=metric[0],
                   namespace=app_name,
                   color=color,
                   dimensions=dim,
                   label='{}.{}.{}'.format(app_name, operation, metric_type),
                   period=Duration.minutes(1),
                   unit=Unit.MILLISECONDS)
