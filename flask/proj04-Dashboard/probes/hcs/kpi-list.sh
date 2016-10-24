#!/bin/bash

#../stg/2016-10/Cust16/hc/20161013-0856/UKXLS2B202016-ccmtemp.txt

path=$1 

preCust=$2
preCmd=$3
preDomain=$4

cmd=`echo $path | sed 's/.*\/.*-//g' | sed 's/.txt//g'` 
pdate=`echo $path | sed 's/.*\/\([0-9]\{8\}-[0-9]\+\).*/\1/g'` 
ldate="${pdate:0:4}-${pdate:4:2}-${pdate:6:2} ${pdate:9:2}:${pdate:11:2}"
srv=`echo $path | sed 's/.*-[0-9]\{4\}\/\([A-Z0-9]\+\)-.*txt/\1/g'`
domain="/$srv/"
cust=`echo $path | sed 's/.*\/\(C[a-z0-9]*\)\/.*/\1/g'`


if [ "$preCust" != "" ] ; then
  cust=$preCust
fi

if [ "$preCmd" != "" ] ; then
  cmd=$preCmd
fi

if [ "$preDomain" != "" ] ; then
  domain=$preDomain
fi


echo "path: $path"
echo "cmd: $cmd"
echo "cust: $cust"
echo "pdate: $pdate"
echo "ldate: $ldate"
echo "srv: $srv"
echo "domain: $domain"


if [ "$cmd" = "ccmtemp" ] ; then
   kpi="ccmTempNFree"
   cat $path | ./kpi-get.sh $kpi $ldate 
fi

if [ "$cmd" = "load" ] ; then
   kpi="nodeLoadAVG"
   cat $path | ./kpi-get.sh $kpi $ldate
fi


if [ "$cmd" = "processes" ] ; then
   kpi="freeMem"
   cat $path | ./kpi-get.sh $kpi $ldate
fi

