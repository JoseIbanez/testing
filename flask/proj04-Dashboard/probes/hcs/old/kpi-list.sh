#!/bin/bash

#../stg/2016-10/Cust16/hc/20161013-0856/UKXLS2B202016-ccmtemp.txt

OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:


while getopts "h?vp:c:d:f:z:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  verbose=1
        ;;
    p)  path=$OPTARG
        ;;
    c)  cust=$OPTARG
        ;;
    d)  domain=$OPTARG
        ;;
    f)  cmd=$OPTARG
        ;;
    esac
done

echo "path: $path"
pdate=`echo $path | sed 's/.*\/\([0-9]\{8\}-[0-9]\+\).*/\1/g'`
echo "pdate: $pdate"
ldate="${pdate:0:4}-${pdate:4:2}-${pdate:6:2} ${pdate:9:2}:${pdate:11:2}"
echo "ldate: $ldate"
srv=`echo $path | sed 's/.*-[0-9]\{4\}\/\([A-Z0-9]\+\)-.*txt/\1/g'`

if [ -z ${cmd} ]; then
   cmd=`echo $path | sed 's/.*\/.*-//g' | sed 's/.txt//g'`
fi

if [ -z ${domain} ]; then
    domain="/$srv/"
fi

if [ -z ${cust} ]; then
    cust=`echo $path | sed 's/.*\/\(C[a-z0-9]*\)\/.*/\1/g'`
fi


echo "cmd: $cmd"
echo "cust: $cust"
echo "srv: $srv"
echo "domain: $domain"

#CUCM

if [ "$cmd" = "ccmtemp" ] ; then
   kpi="ccmTempNFree"
   cat $path | ./kpi-get.sh $kpi $ldate
fi

if [ "$cmd" = "load" ] ; then
   kpi="nodeLoadAVG"
   cat $path | ./kpi-get.sh $kpi $ldate
   kpi="highCPUProccess"
   cat $path | ./kpi-get.sh $kpi $ldate
fi

if [ "$cmd" = "perfCCM" ]; then
   kpi="CallsActive"
   cat $path | ./kpi-get.sh $kpi $ldate
   kpi="RegisteredHardwarePhones"
   cat $path | ./kpi-get.sh $kpi $ldate
fi


#Fabric Interconnect

if [ "$cmd" = "processes" ] ; then
   kpi="freeMem"
   cat $path | ./kpi-get.sh $kpi $ldate
fi

echo
