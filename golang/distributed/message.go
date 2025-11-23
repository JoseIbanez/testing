package main

import (
	"encoding/json"
	"log"
	"net"
)


func (msg *Message) print(comment string) {
		log.Printf("%s %v",comment,*msg)
}



func (msg *Message) serialize() []byte {

	b, err := json.Marshal(msg)
	if err != nil {
		log.Printf("%v",err)
		return []byte{}
	}
	return b

}


func (msg *Message) deserialize(data []byte) error {

	err := json.Unmarshal(data, msg)
	if err != nil {
		log.Printf("%v",err)
		return nil
	}
	
	return nil
}


func (msg *Message) send_to_peer(sock *net.UDPConn, peer *Peer) {

	if peer == nil {
		log.Printf("ERROR: send_to_peer, peer nil")
	}
	msg.send_to_address(sock, peer.Address)
}


func (msg *Message) send_to_address(sock *net.UDPConn, address string) {
	addr, _ := net.ResolveUDPAddr("udp", address)
	msg.send_to_UDPAddr(sock, addr)
}

func (msg *Message) send_to_UDPAddr(sock *net.UDPConn, addr  *net.UDPAddr) {
	data := msg.serialize()
	_, _ = sock.WriteToUDP(data, addr)
}
