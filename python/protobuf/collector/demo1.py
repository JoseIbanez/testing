
import metric_pb2 as Metric

my_metric = Metric.Metric(
    domain="test",
    opco = "VFES",
    customer= "test",
    resource= "VF001",
    messageVersion=1,
    eventEpoc=444,
    values= (Metric.Metric.TupleValue( name="cpu", value=300.0)) ,
    tags= [ Metric.Metric.TupleTag(name="site",value="VF001") ]
)
my_metric.opco = "test"


print(my_metric)