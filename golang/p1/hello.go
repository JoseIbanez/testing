package main

import (
	"fmt"
	"log"
	"math"

	"rsc.io/quote"

	"example/greetings"
	"example/myuser"
)

type User struct {
	id   string
	name string
}

func (u User) description() string {
	return u.name
}

type Device struct {
	id       string
	hostname string
}

func (d Device) description() string {
	return d.hostname
}

type MyItem interface {
	description() string
}

func print_this(i MyItem) {
	fmt.Println(i.description())
}

func main() {



	log.SetPrefix("main: ")
	log.SetFlags(0)

	msg4, err := myuser.TestPointer("hi")
	log.Println(err, msg4)


	msg3, err := myuser.LoadJson("Gladys")
	fmt.Println(err, msg3)

	fmt.Println("Hello, 世界")
	fmt.Println(math.Pi)
	fmt.Println(quote.Go())

	msg1, err := greetings.Hello("Gladys")
	if err != nil {
		log.Fatalln(err)
	}

	msg2, err := greetings.Hello("Go")
	if err != nil {
		log.Println(err)
		log.Fatalln(err)
	}
	fmt.Println("--")
	fmt.Println(err, msg1)
	fmt.Println(err, msg2)

}
