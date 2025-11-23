package main

import (
	"encoding/json"
	"fmt"
	"log"
	"slices"
	"strings"
	"time"
)

func (peerList *PeerList) print() error {

	out := make([]string, len(*peerList))

	for i, peer := range *peerList {
		out[i] = peer.to_string()
	}

	log.Printf("Peers:[ %s ]", strings.Join(out, " "))

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

func (peerList *PeerList) del_by_idx(idx int) error {

	if idx >= len(*peerList) {
		log.Printf("Error to delete, idx:%d bigger than len(peerList):%d", idx, len(*peerList))
		return nil
	}

	log.Printf("Peer:%s idx:%d to delete", (*peerList)[idx].Address, idx)

	*peerList = append((*peerList)[:idx], (*peerList)[idx+1:]...)
	return nil

}

func (peerList *PeerList) del_by_ping() error {

	ret := &PeerList{}

	for _, peer := range *peerList {
		if peer.last_ping_in+40 > time.Now().Unix() || peer.counter_ping_out < 3 {
			*ret = append(*ret, peer)
		}
	}

	*peerList = *ret

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

	return fmt.Sprintf("Addr:%s Ping:%d/%d(%d sec ago) Delay:%d", peer.Address, peer.counter_ping_out, peer.counter_ping_in, int(time.Now().Unix()-peer.last_ping_in), peer.Delay)

}

func (node *SystemState) print() {

	out := make([]string, len(*node.peerList))

	for i, peer := range *node.peerList {
		out[i] = peer.to_string()

	}

	log.Printf("Node:%s, peers:[ %s ]", node.Address, strings.Join(out, " "))

}
