delete from kpi where cust="Cust00";

insert into kpi (cust,kpi,domain,value,date) values
                ("Cust00","RegisteredPhones","/",1000,now()),
                ("Cust00","ConfiguredPhones","/SWI",2000,now());

select * from kpi where cust="Cust00";

delete from kpi where cust="Cust00" and value=1000;

select * from kpi where cust="Cust00";

delete from kpi where cust="Cust00";
