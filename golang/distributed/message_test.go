package main

import (
	"log"
	"testing"
)

func TestMsg_ping(t *testing.T) {


	msg := &Message{Command: "ping"}
	msg.print("test")

	buf := msg.serialize()
	log.Printf("test:%s",buf)


	msg1 := &Message{}

	msg1.deserialize(buf)
	msg1.print("test")

	peerList1 := msg1.PeerList
	if peerList1 != nil {
        t.Fatalf("PeerList not nill")
		return
	}
	peerList1.print()


}



func TestMsg_peerlist(t *testing.T) {

	peerList := make(PeerList,0,30)
	peerList.add_address("127.0.0.1:2000")


	msg := &Message{PeerList: peerList}
	msg.print("test2")

	buf := msg.serialize()
	log.Printf("test:%s",buf)


	msg1 := &Message{}

	msg1.deserialize(buf)
	msg1.print("test2")


	peerList1 := msg1.PeerList
	if peerList1 == nil {
        t.Fatalf("PeerList nill")
		return
	}
	peerList1.print()



}
