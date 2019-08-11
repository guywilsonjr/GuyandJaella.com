from aws_cdk import core, aws_cdk.aws_cloudwatch as cw
from site_fuction.site_fuction import METRICS
class AppMetrics(core.Stack):
    def __init__(
            self,
            app: core.App,
            id: str,
            app_name: str,
            list) -> None:
                
        for metric in metrics:
            operation = metric[0]
            metric_type = metric[1]
            color = metric[2]
            cw.Metric(metric_name=metric[0], 
            namespace=app_name, 
            color=color,
            dimensions=metric, 
            label='{}.{}.{}'.format(app_name, operation, metric_type),
            period=core.Duration.minutes(1),
            unit='Milliseconds')