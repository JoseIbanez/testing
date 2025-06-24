package main

import (
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
)

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	cfg, err := GetConfig()
	if err != nil {
		log.Fatalf("Error getting config: %s", err)
	}

	es, err := elasticsearch.NewClient(*cfg)
	if err != nil {
		log.Fatalf("Error getting config: %s", err)
	}
	log.Printf("Client version %s\n", elasticsearch.Version)
	log.Println(es.Info())

	query_template := `	
		"size" : 10000,
		"query" : {
			"range" : {
				"@timestamp" : 
					{"gte" : "%s",
					  "lt" : "%s"}
			}
		},
		"sort": [
			{ "@timestamp": "asc" }
		]`

	date_from_in := "2025-06-12T11:00:00.000Z"
	offset := 1

	t, err := time.Parse(time.RFC3339, date_from_in)
	if err != nil {
		log.Fatalf("Error parsing date: %s", err)
	}
	date_from := t.Format(time.RFC3339)
	date_to := t.Add(time.Hour * time.Duration(offset)).Format(time.RFC3339)

	log.Printf("Parsed date: %s, from:%s to:%s", t, date_from, date_to)
	query := fmt.Sprintf(query_template, date_from, date_to)
	log.Printf("Query: %s", query)

	store, _ := NewStore(StoreConfig{
		Client:    es,
		IndexName: "cisco-vmanage-pm-metrics",
	})

	last_sort := ""
	var result []string

	fo, err := os.Create("output.jsonl")
	if err != nil {
		panic(err)
	}
	defer func() {
		if err := fo.Close(); err != nil {
			panic(err)
		}
	}()

	for {
		result, last_sort, err = store.search(query, last_sort)

		if err != nil {
			log.Printf("Error searching: %s", err)
			break
		}

		if len(result) == 0 {
			log.Println("End of results")
			break
		}

		// write a chunk
		if _, err := fo.Write([]byte(strings.Join(result, "\n") + "\n")); err != nil {
			panic(err)
		}

	}

}

func GetConfig() (*elasticsearch.Config, error) {

	es_url := os.Getenv("ES_URL")
	es_username := os.Getenv("ES_USERNAME")
	es_password := os.Getenv("ES_PASSWORD")

	if es_url == "" || es_username == "" || es_password == "" {
		return nil, errors.New("environment variables ES_URL, ES_USERNAME, and ES_PASSWORD must be set")
	}

	cfg := elasticsearch.Config{
		Addresses: []string{
			es_url,
		},
		Username: es_username,
		Password: es_password,
	}

	return &cfg, nil
}
