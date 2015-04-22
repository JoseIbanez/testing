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
	icon_image			base/ubuntu.png
	statusmap_image			base/ubuntu.png
	}


###############################################################################
