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
		return "", err
	}
	fmt.Println("Successfully Opened users.json")

	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()

	byteValue, err := io.ReadAll(jsonFile)
	if err != nil {
		fmt.Println(err)
		return "", err
	}

	query := "users.1"
	value := gjson.GetBytes(byteValue, query)
	println(string(value.Raw))

	var raw []byte
	if value.Index > 0 {
		raw = byteValue[value.Index : value.Index+len(value.Raw)]
	} else {
		raw = []byte(value.Raw)
	}
	fmt.Printf("Query:%s result:%s\n", query, raw)

	value2 := gjson.GetBytes(raw, "name")
	fmt.Printf("name: %s\n", value2.String())

	value3 := gjson.GetBytes(raw, "age")
	fmt.Printf("age: %d\n", value3.Int())

	return "hi", nil

}
