## Created by jinja template for nagios host 
## by jose.ibanez@fibratel.com
## Host: {{ hostname}} 

define host {
	host_name			    {{ hostname }}
	use				        xiwizard_genericnetdevice_host
	address				    {{ ip }}
	hostgroups			    {{ hostgroups }}
	max_check_attempts		5
	check_interval			5
	retry_interval			1
	contacts			    nagiosadmin
	notification_interval		4320
	first_notification_delay	0
	notification_options		d,u,r,f,s
	notifications_enabled		1
	icon_image			    network_node.png
	statusmap_image			network_node.png
	_xiwizard			    genericnetdevice
	register			    1
	}	

###############################################################################
