package main

import (
	"testing"
)

func TestPeer_add_address(t *testing.T) {


	peerList := make(PeerList,0,30)

	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2001")
  
    if len(peerList) !=2 {
        t.Fatalf("len(PeerList)=%d", len(peerList))
    }

	peerList.print()

}



