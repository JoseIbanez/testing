package main

import (
	"example/greetings"
	"fmt"
	"log"
	"math"
	"os"

	"io/ioutil"

	"github.com/tidwall/gjson"

	"rsc.io/quote"
)

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
