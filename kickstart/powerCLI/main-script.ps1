deploy-tropo -name "tropo.01" -h "EX11" -storage "CDHP"  -cores 2 -ram 2 -disk 10 -rMHz 100
deploy-tropo -name "tropo.02" -h "EX12" -storage "CDWD"  -cores 4 -ram 4 -disk 40 -rMHz 100
deploy-tropo -name "tropo.03" -h "EX31" -storage "CDWD"  -cores 1 -ram 1 -disk 20 -rMHz 100
deploy-tropo -name "tropo.04" -h "EX32" -storage "CDHP"  -cores 1 -ram 1 -disk 10 -rMHz 100
deploy-tropo -name "tropo.05" -h "EX11" -storage "CDHP"  -cores 2 -ram 2 -disk 10 -rMHz 100
deploy-tropo -name "tropo.06" -h "EX12" -storage "CDWD"  -cores 4 -ram 4 -disk 40 -rMHz 100
deploy-tropo -name "tropo.07" -h "EX31" -storage "CDWD"  -cores 1 -ram 1 -disk 20 -rMHz 100
deploy-tropo -name "tropo.08" -h "EX32" -storage "CDHP"  -cores 1 -ram 1 -disk 10 -rMHz 100



stop-vm -vm "tropo.01" -confirm:$false
stop-vm -vm "tropo.02" -confirm:$false
stop-vm -vm "tropo.03" -confirm:$false
stop-vm -vm "tropo.04" -confirm:$false
stop-vm -vm "tropo.05" -confirm:$false
stop-vm -vm "tropo.06" -confirm:$false
stop-vm -vm "tropo.07" -confirm:$false
stop-vm -vm "tropo.08" -confirm:$false



boot-hd -name "tropo.01"
boot-hd -name "tropo.02"
boot-hd -name "tropo.03"
boot-hd -name "tropo.04"
boot-hd -name "tropo.05"
boot-hd -name "tropo.06"
boot-hd -name "tropo.07"
boot-hd -name "tropo.08"




start-vm -vm "tropo.01" 
start-vm -vm "tropo.02" 
start-vm -vm "tropo.03" 
start-vm -vm "tropo.04" 
start-vm -vm "tropo.05" 
start-vm -vm "tropo.06" 
start-vm -vm "tropo.07" 
start-vm -vm "tropo.08" 


Invoke-VMScript -ScriptText "df" -VM "tropo.01"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.02"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.03"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.04"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.05"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.06"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.07"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.08"-GuestUser root -GuestPassword passw0rd

