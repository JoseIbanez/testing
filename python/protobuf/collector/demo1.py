
from metric_pb2 import Metric

my_metric = Metric(
    domain="test",
    opco = "VFES",
    customer= "test",
    resource= "VF001",
    messageVersion=1,
    eventEpoc=444,
)

my_metric.values.extend([ Metric.Value( name="cpu", value=300.0), Metric.Value( name="mem", value=100.0) ])
my_metric.tags.extend([   Metric.Tag(name="site",value="VF001")  ])

print(my_metric.SerializeToString())

print(my_metric)