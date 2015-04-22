## Created by jinja template for nagios host 
## by jose.ibanez@fibratel.com
## Group: {{ group }} 

define hostgroup {
        hostgroup_name  {{ group }}
        alias           {{ group }}
        }


###############################################################################
