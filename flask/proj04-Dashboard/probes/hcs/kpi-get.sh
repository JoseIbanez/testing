#!/bin/bash

kpi=$1
ldate=$2


if [ "$kpi" = "ccmTempNFree" ]; then
        echo "kpi: $kpi"
	grep [0-9] | sed 's/.*[0-9]\+ \+\([0-9]\+\)/\1/'
	echo
fi

if [ "$kpi" = "nodeLoadAVG" ]; then
	echo "kpi: $kpi" 
        cat $path | grep "average:" | sed "s/.*load average: //"  | cut -d , -f 1
	echo
fi

if [ "$kpi" = "highCPUProccess" ]; then
        echo "kpi: $kpi" 
	cat $path | grep -c -e ' [A-Z] [1-9][0-9][0-9]\.[0-9] ' -e ' [A-Z] [8-9][0-9]\.[0-9] '
	echo
fi


if [ "$cmd" = "perfCCM" ]; then
        echo "#KPI: CallsActive" 
        cat $path | grep " CallsActive " | sed 's/.*= //g'
        echo

        echo "#KPI: RegisteredHardwarePhones"
        cat $path | grep " RegisteredHardwarePhones " | sed 's/.*= //g'
	echo
fi

if [ "$cmd" = "coredump" ]; then
        echo "#KPI: CoreDumpFiles"
	cat $path | grep -c "core\." 
	echo

        echo "#KPI: FreshCoreDump"
        cat $path | grep "core\." | sed 's/[0-9]\+ .B//g' | \
		awk -v today="$ldate" -v period=10  -f ./datediff.awk | grep -c .
	echo

fi

if [ "$kpi" = "freeMem" ]; then
        echo "kpi: $kpi"
        grep "Mem:.*free" | sed 's/.* \+\([0-9]\+\)k free.*/\1/'
        echo
fi


