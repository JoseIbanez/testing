#!/bin/bash

kpi=$1
ldate=$2


#CUCM BD

if [ "$kpi" = "ccmTempNFree" ]; then
    echo "kpi: $kpi"
    grep [0-9] | sed 's/.*[0-9]\+ \+\([0-9]\+\)/\1/'
fi

#CUCM load

if [ "$kpi" = "nodeLoadAVG" ]; then
    echo "kpi: $kpi"
    cat $path | grep "average:" | sed "s/.*load average: //" | cut -d , -f 1
fi

if [ "$kpi" = "highCPUProccess" ]; then
    echo "kpi: $kpi"
    cat $path | grep -c -e ' [A-Z] [1-9][0-9][0-9]\.[0-9] ' -e ' [A-Z] [8-9][0-9]\.[0-9] '
fi


#CUCM perfCCM

if [ "$kpi" = "CallsActive" ]; then
    echo "kpi: $kpi"
    cat $path | grep " CallsActive " | sed 's/.*= //g'
fi

if [ "$kpi" = "RegisteredHardwarePhones" ]; then
    echo "kpi: $kpi"
    cat $path | grep " RegisteredHardwarePhones " | sed 's/.*= //g'
fi

#CUCM CoreDumpFiles

if [ "$cmd" = "coredump" ]; then
    echo "#KPI: CoreDumpFiles"
    cat $path | grep -c "core\."

    echo "#KPI: FreshCoreDump"
    cat $path | grep "core\." | sed 's/[0-9]\+ .B//g' | \
    awk -v today="$ldate" -v period=10  -f ./datediff.awk | grep -c .
    echo
fi



#Fabric Interconnect

if [ "$kpi" = "freeMem" ]; then
    echo "kpi: $kpi"
    grep "Mem:.*free" | sed 's/.* \+\([0-9]\+\)k free.*/\1/'
fi
