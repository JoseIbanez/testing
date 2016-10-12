#!/bin/bash


region=$1
path=$2

set -f                      # avoid globbing (expansion of *).
param=(${path//\// })
set +f

pwd=`pwd`
pdate=${param[-1]}
ldate="${pdate:0:4}-${pdate:4:2}-${pdate:6:2} ${pdate:9:2}:${pdate:11:2}"

if [ "$region" = "UK" ]; then
 udate=`date -u "+%F %T" -d "$ldate BST"`
fi

if [ "$region" = "EU" ]; then
 udate=`date -u "+%F %T" -d "$ldate CEST"`
fi



lote=${param[-2]}
cust=${param[-3]}

echo "Region:$region"
echo "Batch:$lote"
echo "Path:$path"
echo "Cust:$cust"
echo "LocalDate:$ldate"
echo "Date:$udate"

cd $path


#Node load average, NodeLoad
kpi="NodeLoad"

echo
echo "KPI:NodeLoad"
grep -H "average:" *-load.txt | sed "s/-load.*average: /,/" | cut -d , -f 1,2 

echo
echo "KPI:HighProccess"
grep -H -e ' [A-Z] [1-9][0-9][0-9]\.[0-9] ' -e ' [A-Z] [2-9][0-9]\.[0-9] ' -e "average:"  *-load.txt | \
         cut -d - -f 1 | \
         sort | uniq -c | \
         awk  'BEGIN {FS=" "}; { print $2 "," $1-1  }'

echo
echo "KPI:CallsActive"
grep -H " CallsActive " *-perfCCM.txt | sed 's/-.*= /,/g'

echo
echo "KPI:RegisteredHardwarePhones"
grep -H " RegisteredHardwarePhones " *-perfCCM.txt | sed 's/-.*= /,/g'


echo
echo "KPI:RegisteredMGCPGateway"
grep -H " RegisteredMGCPGateway " *-perfCCM.txt | sed 's/-.*= /,/g'



echo
echo "KPI:ServicesOOS"
grep -H -e "Commanded Out of Service" -e "^utils service list"  *-services.txt | \
         grep -v " CAR DB\| DRF Master\| CAR Scheduler\|License Manager\|CDR \|SOAP -" | \
         cut -d - -f 1 | \
         sort | uniq -c | \
         awk  'BEGIN {FS=" "}; { print $2 "," $1-1  }'


echo
echo "KPI:FreshCoreDumps"
(grep "core\." *-coredump.txt | sed 's/[0-9]\+ .B//g' | \
         awk -v today="$ldate" -v period=50  -f $pwd/datedif.awk ; \
         grep "^util" *-coredump.txt ) | \
         cut -d - -f 1 | \
         sort | uniq -c | \
         awk  'BEGIN {FS=" "}; { print $2 "," $1-1}'

