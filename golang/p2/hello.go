package main

import (
	"fmt"
<<<<<<< HEAD
	"io/ioutil"
=======
	"io"
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
	"log"
	"os"

	"github.com/tidwall/gjson"
)

func loadJson(filename string) (string, error) {

	log.Println("Starting json analisys")

	jsonFile, err := os.Open("users.json")
	if err != nil {
		return "", err
	}
	log.Println("Successfully Opened users.json")
	defer jsonFile.Close()

<<<<<<< HEAD
	byteValue, _ := ioutil.ReadAll(jsonFile)
=======
	byteValue, _ := io.ReadAll(jsonFile)
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee

	// Search for nested key
	value := gjson.GetBytes(byteValue, "users.0.name")
	println(value.String())
	fmt.Printf("Struct: Type:%s Index:%d Raw:%+v\n", value.Type, value.Index, value)

	// final value or nested json
	var raw []byte
	if value.Index > 0 {
		raw = byteValue[value.Index : value.Index+len(value.Raw)]
	} else {
		raw = []byte(value.Raw)
	}

	value2 := gjson.GetBytes(raw, "name")
	println(string(value2.Raw))

	return "hi", nil

}

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	msg3, err := loadJson("Gladys")
	fmt.Println(err, msg3)

	log.Println(err)

}
