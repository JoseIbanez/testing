package main

import (
	"log"
	"testing"
	"time"
)

func TestPeer_add_address(t *testing.T) {

	peerList := make(PeerList, 0, 30)

	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2001")

	if len(peerList) != 2 {
		t.Fatalf("len(PeerList)=%d", len(peerList))
	}

	peerList.print()

}

func TestPeer_add_address_01(t *testing.T) {

	peerList := make(PeerList, 0, 30)

	peerList.add_address("127.0.0.1:2000")

	aux_add(&peerList, "127.0.0.1:2001")
	aux_add(&peerList, "127.0.0.1:2002")

	if len(peerList) != 3 {
		t.Fatalf("len(PeerList)=%d", len(peerList))
	}

	peerList.print()

}

func TestPeer_del_by_idx(t *testing.T) {

	peerList := make(PeerList, 0, 30)

	peerList.add_address("127.0.0.1:2000")
	aux_add(&peerList, "127.0.0.1:2001")
	aux_add(&peerList, "127.0.0.1:2002")

	peerList.del_by_idx(1)

	if len(peerList) != 2 {
		t.Fatalf("len(PeerList)=%d", len(peerList))
	}

	peerList.print()

}

func TestPeer_del_by_ping(t *testing.T) {

	peerList := make(PeerList, 0, 30)

	peerList.add_address("127.0.0.1:2000")
	peerList.add(&Peer{Address: "127.0.0.1:2001", last_ping_in: time.Now().Unix()})
	aux_add(&peerList, "127.0.0.1:2002")

	peerList.del_by_ping()

	if len(peerList) != 1 {
		t.Fatalf("len(PeerList)=%d", len(peerList))
	}

	peerList.print()

}

func aux_add(peerList *PeerList, addr string) {

	peerList.add_address(addr)

}

func TestPeer_json(t *testing.T) {

	peerList := make(PeerList, 0, 30)

	peerList.add_address("127.0.0.1:2000")
	peerList.add_address("127.0.0.1:2001")

	peerList.print()
	buf := peerList.to_json()

	log.Printf("peerList:%s", buf)

	peerList1 := make(PeerList, 0, 30)
	peerList1.add_from_json(buf)
	peerList1.print()

}
