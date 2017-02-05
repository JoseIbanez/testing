create view hostStatus as

select kpi.cust,kpi.domain,
   ccmLoadAVG1.id as ccmLoadAVG1_id,ccmLoadAVG1.value as ccmLoadAVG1_value,
   ccmNtpStratum.id as ccmNtpStratum_id,ccmNtpStratum.value as ccmNtpStratum_value


from kpi
left join kpi ccmLoadAVG1
       on (ccmLoadAVG1.cust=kpi.cust and
           ccmLoadAVG1.domain=kpi.domain and
           ccmLoadAVG1.kpi="ccmLoadAVG1")

left join kpi ccmNtpStratum
      on (ccmNtpStratum.cust=kpi.cust and
          ccmNtpStratum.domain=kpi.domain and
          ccmNtpStratum.kpi="ccmNtpStratum")

group by kpi.cust,kpi.domain
order by kpi.cust,kpi.domain;

############
create view perfmon as

select kpi.cust,kpi.domain,
   RegisteredHardwarePhones.id as RegisteredHardwarePhones_id,
   RegisteredHardwarePhones.value as RegisteredHardwarePhones_value,
   CallsActive.id as CallsActive_id,
   CallsActive.value as CallsActive_value

from kpi

left join kpi RegisteredHardwarePhones
       on (RegisteredHardwarePhones.cust=kpi.cust and
           RegisteredHardwarePhones.domain=kpi.domain and
           RegisteredHardwarePhones.kpi="RegisteredHardwarePhones")

left join kpi CallsActive
      on (CallsActive.cust=kpi.cust and
          CallsActive.domain=kpi.domain and
          CallsActive.kpi="CallsActive")

group by kpi.cust,kpi.domain
order by kpi.cust,kpi.domain;
