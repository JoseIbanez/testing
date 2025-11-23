package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"time"

	"math/rand"

	"github.com/akamensky/argparse"
)

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
	bs := parser.String("b", "bootstrap", &argparse.Options{Required: false, Help: "bootstrap server"})
	port := parser.Int("p", "port", &argparse.Options{Required: false, Help: "listening port"})

	err := parser.Parse(os.Args)
	if err != nil {
		fmt.Print(parser.Usage(err))
		return
	}

	//log.SetPrefix("main: ")
	log.SetFlags(0)

	if port != nil {
		go server(fmt.Sprintf(":%d", *port), "")
	}

	if bs != nil {
		for i := 1; i <= 5; i++ {

			other := rand.Intn(32000-10000) + 10000
			go server(fmt.Sprintf(":%d", other), *bs)
		}
	}
	//go client()
	//go client()

	time.Sleep(180 * time.Second)

}
