#!/bin/bash


#../stg/2016-10/Cust16/hc/20161013-0856/UKXLS2B202016-ccmtemp.txt

#path=$1 cmd=`echo $path | sed 's/.*\/.*-//g' | sed 's/.txt//g'` 
#pdate=`echo $path | sed 's/.*\/\([0-9]\{8\}-[0-9]\+\).*/\1/g'` 

cmd=$1
pdate=$2
srv=$3


ldate="${pdate:0:4}-${pdate:4:2}-${pdate:6:2} ${pdate:9:2}:${pdate:11:2}"


#echo -e "#Path: $path"
echo -e "#Cmd: $cmd"
echo -e "#pDate: $pdate"
echo -e "#lDate: $ldate"
echo -e "#Srv: $srv"

if [ "$cmd" = "ccmtemp" ]; then
	echo "#KPI: ccmTempNFree"
	cat $path | grep [0-9] | sed 's/.*[0-9]\+ \+\([0-9]\+\)/\1/'
	echo
fi

if [ "$cmd" = "load" ]; then
	echo "#KPI: NodeLoadAVG" 
        cat $path | grep "average:" | sed "s/.*load average: //"  | cut -d , -f 1
	echo

        echo "#KPI: HighCPUProccess" 
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
