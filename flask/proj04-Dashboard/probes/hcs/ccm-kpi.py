#!/usr/bin/python


#/mnt/tmp/stg/2016-10/Cust21/hc/20161011-1649


path="/mnt/tmp/stg/2016-10/Cust21/hc/20161011-1649"


pathParm=path.split("/")

date=pathParm[-1]
lote=pathParm[-2]
cust=pathParm[-3]


print date,lote,cust


