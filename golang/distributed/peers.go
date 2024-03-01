package main

import (
	"encoding/json"
	"log"
	"slices"
)


func (peerList *PeerList) print() error {

	for i,peer := range *peerList {

		log.Printf("PEER:%d %s",i,peer.Address)

	}


	return nil
}


func (peerList *PeerList) add_address(address string) error {

	if len(address) == 0 {
		return nil
	}

	err := peerList.add(&Peer{Address: address, Delay: -1, Capacity: 1, lastUpdate: 0})
	return err

}

func (peerList *PeerList) find_by_address(address string) *Peer {
 

	idx := slices.IndexFunc(*peerList, func(c Peer) bool { return c.Address == address })
	if idx < 0 {
		return nil
	}
	return &(*peerList)[idx]

}

func (peerList *PeerList) add(peer *Peer) error {
 

	idx := slices.IndexFunc(*peerList, func(c Peer) bool { return c.Address == peer.Address })
	if idx >= 0 {
		return nil
	}

	*peerList = append(*peerList,*peer)
	log.Printf("New peer:%s",peer.Address)
	return nil

}

func (peerList *PeerList) to_json() []byte {


	b, err := json.Marshal(peerList)
	if err != nil {
		log.Printf("%v",err)
		return []byte{}
	}
	return b

}


func (peerList *PeerList) add_from_json(data []byte) error {


	remoteList := &PeerList{}
	err := json.Unmarshal(data, remoteList)
	if err != nil {
		log.Printf("%v",err)
		return nil
	}
	

	for _,peer := range *remoteList {
		peerList.add(&peer)
	}


	return nil

}


func (peerList *PeerList) add_from_list(remoteList *PeerList) error {

	for _,peer := range *remoteList {
		peerList.add(&peer)
	}

	peerList.print()

	return nil

}

