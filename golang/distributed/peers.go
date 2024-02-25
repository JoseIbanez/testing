package main

import (
	"log"
	"slices"
)


func (peerList *PeerList) print() error {

	for i,peer := range *peerList {

		log.Printf("PEER:%d %s",i,peer.address)

	}


	return nil
}


func (peerList *PeerList) add_address(address string) error {

	if len(address) == 0 {
		return nil
	}

	err := peerList.add(&Peer{address: address, delay: 0, capacity: 0, lastUpdate: 0})
	return err

}



func (peerList *PeerList) add(peer *Peer) error {
 

	idx := slices.IndexFunc(*peerList, func(c Peer) bool { return c.address == peer.address })

	if idx > 0 {
		return nil
	}

	*peerList = append(*peerList,*peer)
	return nil

}