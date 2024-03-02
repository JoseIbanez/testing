package main

import (
	"fmt"
	"log"
	"net"
	"time"
)

func server_send_updates(sock *net.UDPConn, state *SystemState, peerList *PeerList) {

	for {
		time.Sleep(5 * time.Second)

		for i, peer := range *peerList {

			log.Printf("Id:%s idx:%d update to peer:%s", state.Address, i, peer.Address)

			msg := Message{Command: "ping",
				PeerList:    *peerList,
				SystemState: state,
				Ping:        &Ping{A_out: time.Now().UnixMicro()}}
			msg.send_to_peer(sock, &peer)

			time.Sleep(1 * time.Second)

		}
	}

}

func server_send_pong(sock *net.UDPConn, state *SystemState, raddr *net.UDPAddr, ping *Ping, received_micro int64) {

	ping.B_in = received_micro
	ping.B_out = time.Now().UnixMicro()

	msg := &Message{Command: "pong", Ping: ping}
	msg.send_to_UDPAddr(sock, raddr)

}

func update_peer_delay(state *SystemState, raddr *net.UDPAddr, ping *Ping, received_micro int64) {

	ping.A_in = received_micro

	total_delay := ping.A_in - ping.A_out
	remote_delay := ping.B_out - ping.B_in

	rAddress := fmt.Sprintf("%s:%d", raddr.IP, raddr.Port)

	log.Printf("Node:%s delay to Peer:%s, total:%d, remote:%d, network:%d", state.Address, rAddress, total_delay, remote_delay, total_delay-remote_delay)

	peer := state.peerList.find_by_address(rAddress)
	if peer == nil {
		return
	}

	peer.Delay = int(total_delay - remote_delay)
	log.Printf("Node:%s, peer updated:%v", state.Address, *peer)

}
