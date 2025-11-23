package main

import (
	"bufio"
	"compress/gzip"
	"fmt"
	"log"
	"os"

	"github.com/tidwall/gjson"
)

func readLinesFromGZ(filename string) ([]string, error) {

	log.Println("Opening file:", filename)
	filePath := fmt.Sprintf("sample_data/%s", filename)
	fi, err := os.Open(filePath)
	if err != nil {
		log.Fatalf("Error opening file: %v", err)
		return nil, err
	}
	defer fi.Close()

	fz, err := gzip.NewReader(fi)
	if err != nil {
		log.Fatalf("Error opening file: %v", err)
		return nil, err
	}
	defer fz.Close()

	bufferedContents := bufio.NewReader(fz)

	lines := []string{}
	for {
		line, err := bufferedContents.ReadString('\n')
		if err != nil {
			break
		}
		lines = append(lines, line)
	}
	return lines, nil
}

type Counter struct {
	Id        string  `json:"id"`
	Timestamp string  `json:"timestamp"`
	Name      string  `json:"name"`
	Value     float64 `json:"value"`
}

// Parse counter json
func parseJson(byteValue []byte) ([]Counter, error) {

	var result []Counter

	id := gjson.GetBytes(byteValue, "_id").Str
	timestamp := gjson.GetBytes(byteValue, "_source.pm_data_source.timestamp").Str
	//log.Printf("ID: %s Timestamp: %s", id, timestamp)

	counterMap := gjson.GetBytes(byteValue, "_source.pm_data").Map()
	for k, v := range counterMap {
		//fmt.Printf("%s: %v\n", k, v)
		counter := Counter{id, timestamp, k, v.Float()}
		result = append(result, counter)
	}

	return result, nil

}

func parseList(input []string) ([]Counter, error) {

	var result []Counter

	for _, line := range input {

		counterList, err := parseJson([]byte(line))
		if err != nil {
			continue
		}

		for _, counter := range counterList {
			log.Printf("Counter: %v", counter)
			result = append(result, counter)
		}

	}
	return result, nil

}

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	lines, err := readLinesFromGZ("radio-pm.jsonl.gz")
	fmt.Println(err, len(lines))

	result, err := parseJson([]byte(lines[0]))
	fmt.Println(result, err)

	_, err = parseList(lines)
	fmt.Println(err)

}
