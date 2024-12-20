package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/tidwall/gjson"
)

type Price struct {
	Value        float32 `json:"value"`
	Datetime_utc string  `json:"datetime_utc"`
	Geo_name     string  `json:"geo_name"`
}

func updatePrice(p *Price) (err error) {
	p.Value = p.Value * 1.1
	return nil
}

// loads a file and parses a nested json array
//
// filename: string
// return: string, error
// Example:
// loadJson("1001.json")
// returns: "Done", nil
func loadJson(filename string) (string, error) {
	//Some documentation

	log.Println("Starting json analisys")

	filePath := fmt.Sprintf("sample_data/%s", filename)
	jsonFile, err := os.Open(filePath)
	if err != nil {
		return "", err
	}

	log.Printf("Successfully Opened %s\n", filename)
	defer jsonFile.Close()

	byteValue, _ := io.ReadAll(jsonFile)

	// Search for nested key
	value := gjson.GetBytes(byteValue, "indicator.values")
	//println(value.String())
	log.Printf("Struct: Type:%s Index:%d", value.Type, value.Index)
	//fmt.Printf("Raw: %+v\n", value.Raw)

	// final value or nested json
	var raw []byte
	if value.Index > 0 {
		raw = byteValue[value.Index : value.Index+len(value.Raw)]
	} else {
		raw = []byte(value.Raw)
	}

	//parse json array
	var arr []Price
	_ = json.Unmarshal(raw, &arr)
	//log.Printf("Unmarshaled: %v", arr)

	//iterate over price array
	for _, p := range arr {
		if p.Geo_name != "Península" {
			continue
		}

		err := updatePrice(&p)
		if err != nil {
			log.Fatalf("Error updating price: %v", err)
			return "", err
		}

		log.Printf("Price: %f, Date: %s", p.Value, p.Datetime_utc)
	}

	return "Done", nil

}

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	msg3, err := loadJson("1001.json")
	fmt.Println(err, msg3)

	log.Println(err)

}
