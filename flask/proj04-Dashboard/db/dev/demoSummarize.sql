insert ignore into log
select Cust,kpi,"/",sum(value),date
from log
where kpi='RegisteredHardwarePhones' and domain<>"/"
group by cust,kpi,date;

insert ignore into log
select Cust,kpi,"/",sum(value),date
from log
where kpi='CallsActive' and domain<>"/"
group by cust,kpi,date;



insert ignore into kpi
(cust,kpi,domain,value,date)
select Cust,kpi,"/",sum(value),date
from kpi
where kpi='RegisteredHardwarePhones' and domain<>"/"
group by cust,kpi,date;

insert ignore into kpi
(cust,kpi,domain,value,date)
select Cust,kpi,"/",sum(value),date
from kpi
where kpi='CallsActive' and domain<>"/"
group by cust,kpi,date;


delete from log where domain="/" and value=0;
