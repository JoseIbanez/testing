package main

import (
<<<<<<< HEAD
	"example/greetings"
	"fmt"
	"log"
	"math"
	"os"

	"io/ioutil"

	"github.com/tidwall/gjson"

	"rsc.io/quote"
=======
	"fmt"
	"log"
	"math"

	"rsc.io/quote"

	"example/greetings"
	"example/myuser"
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
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

<<<<<<< HEAD
func loadJson(filename string) (string, error) {
	jsonFile, err := os.Open("users.json")
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")

	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	value := gjson.GetBytes(byteValue, "users.1")
	println(string(value.Raw))

	var raw []byte
	if value.Index > 0 {
		raw = byteValue[value.Index : value.Index+len(value.Raw)]
	} else {
		raw = []byte(value.Raw)
	}
	println(raw)

	value2 := gjson.GetBytes(raw, "name")
	println(string(value2.Raw))

	return "hi", nil

}

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	msg3, err := loadJson("Gladys")
=======
func main() {



	log.SetPrefix("main: ")
	log.SetFlags(0)

	msg4, err := myuser.TestPointer("hi")
	log.Println(err, msg4)


	msg3, err := myuser.LoadJson("Gladys")
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
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
