package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"strings"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
)

type StoreConfig struct {
	Client    *elasticsearch.Client
	IndexName string
}

type Store struct {
	es        *elasticsearch.Client
	indexName string
}

func NewStore(c StoreConfig) (*Store, error) {
	indexName := c.IndexName

	s := Store{es: c.Client, indexName: indexName}
	return &s, nil
}

func (s *Store) buildQuery(query string, after string) io.Reader {
	var b strings.Builder

	b.WriteString("{\n")

	b.WriteString(query)

	if len(after) > 0 {
		b.WriteString(",\n")
		b.WriteString(fmt.Sprintf(`	"search_after": %s`, after))
	}

	b.WriteString("\n}")

	// fmt.Printf("%s\n", b.String())
	return strings.NewReader(b.String())
}

func (s *Store) search(query string, after string) ([]string, string, error) {

	time0 := time.Now().UnixMilli()

	q := s.buildQuery(query, after)
	//log.Printf("Query: %s", q)

	res, err := s.es.Search(
		s.es.Search.WithIndex(s.indexName),
		s.es.Search.WithBody(q),
		s.es.Search.WithTrackTotalHits(true),
	)
	if err != nil {
		log.Fatalf("Error getting response: %s", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		log.Fatalf("Error: %s", res.String())
	}

	//log.Printf("Response: %s", res.String())

	time1 := time.Now().UnixMilli()
	log.Printf("Search took %d ms", time1-time0)

	var r map[string]interface{}

	json.NewDecoder(res.Body).Decode(&r)

	hits := r["hits"].(map[string]interface{})["hits"].([]interface{})

	var last_sort []interface{}

	var results []string

	for _, hit := range hits {
		last_sort = hit.(map[string]interface{})["sort"].([]interface{})
		strH, _ := json.Marshal(hit)
		results = append(results, string(strH))
	}
	strSort, _ := json.Marshal(last_sort)
	time1 = time.Now().UnixMilli()
	log.Printf("Got %d hits, last sort %s, process took %d ms", len(hits), string(strSort), time1-time0)

	return results, string(strSort), nil
}
