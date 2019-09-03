import os
from aws_cdk.core import App, Stack, Duration
from aws_cdk.aws_cloudwatch import Metric, Unit
from site_function.site_utils import METRICS, METRIC_NAME_FORMAT, get_metric_name

stage = 'DEV'
if 'PROD' in os.environ:
    stage = 'PROD'
    
class AppMetrics(Stack):
    def __init__(
            self,
            app: App,
            id: str,
            app_name: str,
            metrics: list) -> None:
        super().__init__(app, id)
        for metric in metrics:
            operation = metric[0]
            metric_type = metric[1]
            color = metric[3]

            dim = {
                'By App Version': os.environ['APP_VERSION'],
                'By Operation': operation,
                'By Stage': stage}

            Metric(metric_name=get_metric_name(metric=metric),
                   namespace=app_name,
                   color=color,
                   dimensions=dim,
                   period=Duration.minutes(1),
                   unit=Unit.MILLISECONDS)
