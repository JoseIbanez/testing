package main

import (
	"encoding/json"
	"fmt"
	"log"
	"slices"
	"strings"
)

func (peerList *PeerList) print() error {

	for i, peer := range *peerList {
		log.Printf("PEER:%d %s", i, peer.Address)
	}

	return nil
}

func (peerList *PeerList) add_address(address string) error {

	if len(address) == 0 {
		log.Printf("bad address %s", address)
		return nil
	}

	err := peerList.add(&Peer{Address: address, Delay: -1, Capacity: 1})
	return err

}

func (peerList *PeerList) find_by_address(address string) *Peer {

	idx := slices.IndexFunc(*peerList, func(c Peer) bool { return c.Address == address })
	if idx < 0 {
		log.Printf("Not found, peer:%s, peerlist:%v", address, peerList)
		return nil
	}
	return &(*peerList)[idx]

}

func (peerList *PeerList) add(peer *Peer) error {

	idx := slices.IndexFunc(*peerList, func(c Peer) bool { return c.Address == peer.Address })
	if idx >= 0 {
		return nil
	}

	*peerList = append(*peerList, *peer)
	log.Printf("New peer:%s", peer.Address)
	return nil

}

func (peerList *PeerList) to_json() []byte {

	b, err := json.Marshal(*peerList)
	if err != nil {
		log.Printf("%v", err)
		return []byte{}
	}
	return b

}

func (peerList *PeerList) add_from_json(data []byte) error {

	remoteList := &PeerList{}
	err := json.Unmarshal(data, remoteList)
	if err != nil {
		log.Printf("%v", err)
		return nil
	}

	for _, peer := range *remoteList {
		peerList.add(&peer)
	}

	return nil

}

func (peerList *PeerList) add_from_list(remoteList *PeerList) error {

	for _, peer := range *remoteList {
		peerList.add(&peer)
	}

	return nil

}

func (peer *Peer) to_string() string {

	return fmt.Sprintf("Addr:%s Ping:%d/%d Delay:%d", peer.Address, peer.counter_ping_out, peer.counter_ping_in, peer.Delay)

}

func (node *SystemState) print() {

	out := make([]string, len(*node.peerList))

	for i, peer := range *node.peerList {
		out[i] = peer.to_string()

	}

	log.Printf("Node:%s, peers:[ %s ]", node.Address, strings.Join(out, " "))

}
