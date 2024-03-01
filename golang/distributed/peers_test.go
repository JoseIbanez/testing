package main

import (
	"log"
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


func TestPeer_json(t *testing.T) {


	peerList := make(PeerList,0,30)

	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2001")

	peerList.print()
	buf := peerList.to_json()

	log.Printf("peerList:%s",buf)

	peerList1 := make(PeerList,0,30)
	peerList1.add_from_json(buf)
	peerList1.print()

}


