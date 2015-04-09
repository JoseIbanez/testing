define service {
        host_name                       MT_MOXA_GRAN_VIA
        service_description             Trafico de nodo Desengano
        use                             xiwizard_generic_service
        check_command                   check_iftraffic3!public!6!100!!!!!
        register                        1
        }
