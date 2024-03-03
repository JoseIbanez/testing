package main

import (
	"fmt"
	"log"
	"net"
	"time"

	"github.com/google/uuid"
)

func server(source string, bs string) {

	//log.SetPrefix(source)

	addr, err := net.ResolveUDPAddr("udp", source)
	if err != nil {
		fmt.Println(err)
		return
	}

	sock, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Println(err)
		return
	}

	peerList := make(PeerList, 0, 30)
	peerList.add_address(bs)

	state := SystemState{peerList: &peerList, Address: source, Id: uuid.New().String(), StreamId: "1111"}

	go server_listen(sock, &state, &peerList)
	go send_ping(sock, &state, &peerList)

	//fmt.Printf("peerList: %v\n", peerList)

}

func server_listen(sock *net.UDPConn, state *SystemState, peerList *PeerList) {

	for {
		buf := make([]byte, 1024)
		rlen, raddr, err := sock.ReadFromUDP(buf)
		received_micro := time.Now().UnixMicro()
		if err != nil {
			fmt.Println(err)
		}

		log.Printf("%s <- %s:%d, msg:%s", state.Address, raddr.IP, raddr.Port, string(buf[0:rlen]))

		// Add new peer to the list
		peerAddress := fmt.Sprintf("%s:%d", raddr.IP, raddr.Port)
		peerList.add_address(peerAddress)

		// Analize message
		msg := &Message{}
		msg.deserialize(buf[0:rlen])

		if msg.Command == "ping" {
			send_pong(sock, state, raddr, msg.Ping, received_micro)
		}

		if msg.Command == "pong" {
			update_peer_delay(state, raddr, msg.Ping, received_micro)
		}

		if msg.PeerList != nil {
			peerList.add_from_list(&msg.PeerList)
		}

		//Clean up
		state.peerList.del_by_ping()

		state.print()

	}
}
