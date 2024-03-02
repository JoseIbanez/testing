package main

import (
	"testing"

	"github.com/google/uuid"
)

func TestServer_print(t *testing.T) {

	bs := "127.0.0.1:2000"
	source := ":2000"

	peerList := make(PeerList, 0, 30)
	peerList.add_address(bs)

	state := SystemState{peerList: &peerList, Address: source, Id: uuid.New().String(), StreamId: "1111"}

	state.print()

}
