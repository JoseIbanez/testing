

System = require('console')
//System=[];
//System.log = (log)  => { print(log) }; 

newCdir = 28;


poolData = [{"id":"152","network":"33.33.33.33","mask":"255.255.255.0","cidr":24,"cramerMask":"255.255.255.192","cramerCidr":26,"cramerRange":"33.33.33.33","cramerSpace":"Vodafone Address Space"}]
subnets = [{"subnetId":"197","dlrName":"DE1CIVB12XDLR01-1.VOD","portgroup":"vxw-dvs-49-virtualwire-185-sid-10115-vx-nsx_33_33_33_80_26","ipamRef":"TP.VOD.vx-nsx_33_33_33_80_26"},{"subnetId":"204","dlrName":"MyDLR","portgroup":"vxw-dvs-49-virtualwire-191-sid-10104-vx-nsx_33_33_33_0_30","ipamRef":"TP.VOD.vx-nsx_33_33_33_0_30"},{"subnetId":"599","dlrName":"DE1XDLR01-1.VOD","portgroup":"vxw-dvs-50-virtualwire-327-sid-5160-vx-nsx_33_33_33_4_30","ipamRef":"TD.VOD.vx-nsx_33_33_33_4_30"},{"subnetId":"612","dlrName":"DE1XDLR01-1.VOD","portgroup":"vxw-dvs-50-virtualwire-339-sid-5159-vx-nsx_33_33_33_8_30","ipamRef":"TD.VOD.vx-nsx_33_33_33_8_30"},{"subnetId":"614","dlrName":"DE1XDLR01-1.VOD","portgroup":"vxw-dvs-50-virtualwire-341-sid-5159-vx-nsx_33_33_33_12_30","ipamRef":"TD.VOD.vx-nsx_33_33_33_12_30"},{"subnetId":"631","dlrName":"DE1CIVB12XDLR01-1.VOD","portgroup":"vxw-dvs-104-virtualwire-202-sid-10075-vx-nsx_33_33_33_16_30","ipamRef":"TD.VOD.vx-nsx_33_33_33_16_30"},{"subnetId":"632","dlrName":"DE1XDLR01-1.VOD","portgroup":"vxw-dvs-50-virtualwire-354-sid-5161-vx-nsx_33_33_33_20_30","ipamRef":"TD.VOD.vx-nsx_33_33_33_20_30"}]

poolMask    = poolData[0].mask;
poolNetwork = int2ip( ip2int(poolData[0].network) & ip2int(poolData[0].mask))
poolCidr    = poolData[0].cidr;

poolMin = int2ip( ip2int(poolNetwork) & ip2int(poolData[0].mask) )
poolMax = int2ip( ip2int(poolNetwork) | ~ ip2int(poolMask) )
System.log("Pool: "+poolNetwork+"/"+poolCidr);
System.log("Pool: "+poolMin+" - "+poolMax);







subnetByIp = [];

for (var i in subnets) {
    item = subnets[i];

    System.log(item.subnetId+", "+item.ipamRef);
    
    //[net, cdir] = getPgInfo(item.ipamRef);
    ret = getPgInfo(item.ipamRef);
    net = ret[0]
    cdir = ret[1]
    
	maskInt =  (~0) << (32-cdir) >>> 0;
    item.netInt = (ip2int(net) & maskInt) >>>0;
	item.cdir= cdir;
	item.network = net;
    subnetByIp.push([item.ipamRef, item])
}


subnetByIp.sort(function (a,b) { return a[1].netInt - b[1].netInt });
//System.log(subnetByIp);

newNet = ip2int(poolMin);
poolMaxInt = ip2int(poolMax)

index = 0;

// Search in the pool for a new subnet site
while (newNet < poolMaxInt) {

    System.log("Trying ... "+int2ip(newNet));


	if (index >= subnetByIp.length) {
        System.log("Site found "+int2ip(newNet));
        newNet += Math.pow(2, 32 - newCdir);
        continue;
    }
    	
    curNet=subnetByIp[index][1];
    curNetSize = Math.pow(2, 32 - curNet.cdir);
    newNetSize = Math.pow(2, 32 - newCdir);

	//System.log(curNet.network);

    if (curNet.netInt + curNetSize - 1 < newNet) {
        System.log("Below "+curNet.network);
        index ++;
        continue;
    }


    if (netCheckOverlap(newNet,newCdir,curNet.netInt,curNet.len)) {
        System.log("Overlap "+curNet.network);
        inc = newNetSize > curNetSize ? newNetSize : curNetSize;
        newNet += inc;
        //System.log("inc:"+inc+", newNet:"+newNet);
        continue;
    }

    System.log("Site found "+int2ip(newNet));
    newNet += Math.pow(2, 32 - newCdir);


}



function getPgInfo(portgroupName) {
	res = portgroupName.match(/(\d+)_(\d+)_(\d+)_(\d+)_(\d+)$/);
	net = res[1]+"."+res[2]+"."+res[3]+"."+res[4];
	len = parseInt(res[5]);
	return [net,len];
};

													
function netCheckOverlap(n1Int,len1,n2Int,len2) {
	m1Int =  (~0) << (32-len1) >>> 0;
	m2Int =  (~0) << (32-len2) >>> 0;

	r1 = (n1Int & m1Int & m2Int) >>>0;
	r2 = (n2Int & m1Int & m2Int) >>>0;

	if ( r1==r2 ) {
		//System.log("Net overlap: "+int2ip(n1Int)+", "+int2ip(n2Int)+".");
		return true;
	} else {
		return false;
	}
}


function fromLen2netmask(len) {
	maskInt = (~0) << (32-len) >>> 0;
	return int2ip(maskInt);
}

function getFristIpNetwork(network, len) {

	ipInt = ip2int(network);
	maskInt = (~0) << (32-len) >>> 0;
	gatewayInt = ( ipInt & maskInt ) + 1;
	
	return int2ip(gatewayInt);
}


function ip2int(ip) {
	ip = ip.replace(/_/g, ".").replace("/",".");
	a1=ip.split(".")
	if (a1.length == 5) a1.pop();
    return a1.reduce(function(ipInt, octet) { return (ipInt<<8) + parseInt(octet, 10) }, 0) >>> 0;
}																		
																																																						
function int2ip (ipInt) {
    return ( (ipInt>>>24) +'.' + (ipInt>>16 & 255) +'.' + (ipInt>>8 & 255) +'.' + (ipInt & 255) );
}
																																																		
function toHex(d) {
    return  ("00000000"+(Number(d).toString(16))).slice(-8).toUpperCase()
}

