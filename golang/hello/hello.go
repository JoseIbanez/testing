package main

import (
	"fmt"
	"log"

	"example.com/greetings"
	"rsc.io/quote"
)

func main() {

	log.SetPrefix("greetings: ")
	log.SetFlags(0)
	log.Output(2, "Starting")

	fmt.Println(quote.Go())
	a, err := greetings.Hello("p1")
	if err != nil {
		log.Fatal(err)
	}

	b, err := greetings.Hello2("p2")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(a)
	fmt.Println(b)
}
