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

  //peerList := make([]Peer,0,30)
  peerList := make(PeerList,0,30)

  peerList.add_address(bs)

  go server_listen(sock,addr,&peerList)


  fmt.Printf("peerList: %v\n", peerList)

  for {
	time.Sleep(1 * time.Second)
	for i,peer := range peerList {


		log.Printf("PING %d peer:%s",i,peer.address)

		raddr, _ := net.ResolveUDPAddr("udp", peer.address)
		_, _ = sock.WriteToUDP([]byte("ping"), raddr)

		time.Sleep(1 * time.Second)

	}
  }

}

func server_listen(sock *net.UDPConn, laddr *net.UDPAddr, peerList *PeerList) {

  for {
    buf := make([]byte, 1024)
    rlen, raddr, err := sock.ReadFromUDP(buf)
    if err != nil {
      fmt.Println(err)
    }

	log.Printf("%s:%d <- %s:%d, msg:%s", laddr.IP, laddr.Port ,raddr.IP,raddr.Port,string(buf[0:rlen]))



    //go handlePacket(buf, rlen)
	//_, _ = sock.WriteToUDP([]byte("pong"), raddr)

	peerList.add_address(fmt.Sprintf("%s:%d",raddr.IP,raddr.Port))

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

	time.Sleep( 15 * time.Second)

}