package main

import (
	"errors"
	"log"
	"os"
	"strings"

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

	query := `	
		"size" : 10000,
		"query" : {
			"range" : {
				"@timestamp" : 
					{"gte" : "2025-06-14T00:00:00.000Z",
					  "lt" : "2025-06-15T00:00:00.000Z"}
			}
		},
		"sort": [
			{ "@timestamp": "asc" }
		]`

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

	for i := 0; i < 100; i++ {

		result, last_sort, err = store.search(query, last_sort)

		if err != nil {
			log.Printf("Error searching: %s", err)
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
