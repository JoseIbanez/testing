package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"time"

	"github.com/akamensky/argparse"
)

func server(source string, bs string) {

  log.SetPrefix(source)


  addr, err := net.ResolveUDPAddr("udp", source)
  if err != nil {
	fmt.Println(err)
	return
  }

  sock,err := net.ListenUDP("udp", addr)
  if err != nil {
	fmt.Println(err)
	return
  }

  peerList := make(PeerList,0,30)
  peerList.add_address(bs)

  state := SystemState{peerList: peerList, Address: source, StreamId: "1111" }


  go server_listen(sock,&state,&peerList)
  go server_send_updates(sock,&state,&peerList)


  fmt.Printf("peerList: %v\n", peerList)

}






func server_listen(sock *net.UDPConn, state *SystemState, peerList *PeerList) {

  for {
    buf := make([]byte, 1024)
    rlen, raddr, err := sock.ReadFromUDP(buf)
	received_micro := time.Now().UnixMicro()
	if err != nil {
      fmt.Println(err)
    }

	log.Printf("%s <- %s:%d, msg:%s", state.Address ,raddr.IP,raddr.Port,string(buf[0:rlen]))

	// Add new peer to the list
	//peerList.add_address(fmt.Sprintf("%s:%d",raddr.IP,raddr.Port))
	peerList.add(&Peer{Address: fmt.Sprintf("%s:%d",raddr.IP,raddr.Port),
		 			   lastUpdate: time.Now().Unix()})

	// Analize message
	msg := &Message{}
	msg.deserialize(buf[0:rlen])


	if msg.Command == "ping" {
		server_send_pong(sock, state, raddr, msg.Ping, received_micro)
	}

	if msg.Command == "pong" {
		update_peer_delay(state, raddr, msg.Ping, received_micro)
	}


	if  msg.PeerList != nil {
		peerList.add_from_list(&msg.PeerList)
	}



  }
}



func client() {

	//con, _ := net.Dial("udp", "127.0.0.1:2000")

	LocalAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:2001")
	if err != nil {
		fmt.Println(err)
		return
	}
	RemoteEP := net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 2000}
	con, err := net.DialUDP("udp", LocalAddr, &RemoteEP)
	if err != nil {
		fmt.Println(err)
		return
	}

	for i := 0; i < 10000; i++ {


		fmt.Println(".")
		buf := []byte("bla bla bla I am the packet")

		_, err := con.Write(buf)
		if err != nil {
		  fmt.Println(err)
		}

		time.Sleep(10 * time.Millisecond)

	}
}




func main() {

	parser := argparse.NewParser("distributed network", "Deploy a distributed network")
	b := parser.String("b", "string", &argparse.Options{Required: true, Help: "bootstrap server"})

	err := parser.Parse(os.Args)
	if err != nil {
		fmt.Print(parser.Usage(err))
		return
	}

	log.SetPrefix("main: ")
	log.SetFlags(0)


	// Finally print the collected string
	log.Println(*b)

	go server(":2000","")
	go server(":2001","127.0.0.1:2000")
	go server(":2002","127.0.0.1:2000")
	go server(":2003","127.0.0.1:2000")

	//go client()
	//go client()

	time.Sleep( 60 * time.Second)

}