deploy-tropo -name "tropo.01" -h "EX11" -storage "CDHP"  -cores 2 -ram 2 -disk 10 -rMHz 100
deploy-tropo -name "tropo.02" -h "EX12" -storage "CDWD"  -cores 4 -ram 4 -disk 40 -rMHz 100
deploy-tropo -name "tropo.03" -h "EX31" -storage "CDWD"  -cores 1 -ram 1 -disk 20 -rMHz 100
deploy-tropo -name "tropo.04" -h "EX31" -storage "CDHP"  -cores 1 -ram 1 -disk 10 -rMHz 100

stop-vm -vm "tropo.01" -confirm:$false
stop-vm -vm "tropo.02" -confirm:$false
stop-vm -vm "tropo.03" -confirm:$false
stop-vm -vm "tropo.04" -confirm:$false

boot-hd -name "tropo.01"
boot-hd -name "tropo.02"
boot-hd -name "tropo.03"
boot-hd -name "tropo.04"

start-vm -vm "tropo.01" 
start-vm -vm "tropo.02" 
start-vm -vm "tropo.03" 
start-vm -vm "tropo.04" 



