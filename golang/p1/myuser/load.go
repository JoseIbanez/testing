package myuser

import (
	"fmt"
	"io"
	"os"

	"github.com/tidwall/gjson"
)

func LoadJson(filename string) (string, error) {
	jsonFile, err := os.Open("users.json")
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")

	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()

	byteValue, _ := io.ReadAll(jsonFile)

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
