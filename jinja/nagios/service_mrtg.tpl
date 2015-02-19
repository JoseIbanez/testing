## Created by jinja template for nagios "trafico" service
## by jose.ibanez@fibratel.com
## Host: {{ hostname}} Service {{ description }} Port {{ port }}
define service {
        host_name                       {{hostname}}
        service_description             {{description}}
        use                             xiwizard_generic_service
        check_command                   check_local_mrtgtraf_ayuntamiento!{{port}}!AVG!50000000,50000000!70000000,70000000!!!!
        register                        1
        }
