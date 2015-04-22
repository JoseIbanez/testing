## Created by jinja template for nagios host 
## by jose.ibanez@fibratel.com
## Host: {{ hostname}} 

define host {
	host_name			{{ hostname }}
        alias				{{ hostname }}
	use				generic-host
	address				{{ ip }}
	hostgroups			ro,{{ hostgroups }}
	#contacts			nagiosadmin
	icon_image			cook/router.png
	statusmap_image			cook/router.png
	}	

###############################################################################
