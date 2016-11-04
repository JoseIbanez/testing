insert ignore into log
select Cust,kpi,"/",sum(value),date
from log
where kpi='RegisteredHardwarePhones' and domain<>"/"
group by cust,kpi,date;
