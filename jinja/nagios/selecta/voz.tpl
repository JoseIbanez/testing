## Created by jinja template for nagios host 
## by jose.ibanez@fibratel.com
## Host: {{ hostname}} 

define host {
	host_name			{{ hostname }}
        alias				{{ hostname }}
	use				generic-host
	address				{{ ip }}
	hostgroups			srv,{{ hostgroups }}
	#contacts			nagiosadmin
	icon_image			logos/cisco.png
	statusmap_image			logos/cisco.png
	}


###############################################################################
