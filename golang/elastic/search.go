package main

import (
	"bufio"
	"compress/gzip"
	"context"
	"errors"
	"fmt"
	"log"
	"os"
	"os/signal"
	"strings"
	"sync/atomic"
	"syscall"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
	"github.com/jessevdk/go-flags"
)

var (
	buildVersion   = "UNKNOWN"
	isShuttingDown atomic.Bool
)

type ArgsOptions struct {
	DateFrom string `short:"d" long:"date-from" description:"Date from in RFC3339 format, e.g. 2025-06-12T12:00:00Z" required:"true"`
	Index    string `short:"i" long:"index" description:"Index name, e.g. cisco-vmanage-pm-metrics" required:"true"`
	Output   string `short:"o" long:"output" description:"Output forlder name, e.g. ./data/" required:"true"`
	Slot     int    `short:"s" long:"slot" description:"Slot in hours, e.g. 1" required:"true"`
	Verbose  bool   `short:"v" long:"verbose" description:"Enable verbose logging"`
}

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)
	log.Printf("Starting elasticsearch dump tool, version: %s", buildVersion)

	// Capture shutdown signal
	rootCtx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()
	go lisenForShutdown(rootCtx, stop)

	// Parse command line arguments
	opts := getCommandLineArgs()

	// Elasticsearch client config
	cfg, err := getElasticConfig()
	if err != nil {
		log.Fatalf("Error getting config: %s", err)
	}

	es, err := elasticsearch.NewClient(*cfg)
	if err != nil {
		log.Fatalf("Error getting config: %s", err)
	}
	log.Printf("Client version %s\n", elasticsearch.Version)
	log.Println(es.Info())

	store, _ := NewStore(StoreConfig{
		Client:    es,
		IndexName: opts.Index,
	})

	// Get query and filename
	query, filename, err := generateQuery(&opts)
	if err != nil {
		log.Fatalf("Error generating query: %s", err)
	}

	// Query ES and save to file
	err = saveToFile(store, query, opts.Output, filename)
	if err != nil {
		log.Fatalf("Error saving to file: %s", err)
	}

}

func generateQuery(opts *ArgsOptions) (string, string, error) {

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

	// date_form and date_to
	t, err := time.Parse(time.RFC3339, opts.DateFrom)
	if err != nil {
		return "", "", fmt.Errorf("error parsing date: %w", err)
	}
	date_from := t.Format(time.RFC3339)
	date_to := t.Add(time.Hour * time.Duration(opts.Slot)).Format(time.RFC3339)
	filename := fmt.Sprintf("o-%s.jsonl", t.Format("20060102-15"))

	log.Printf("Parsed date: %s, from:%s to:%s, file:%s", t, date_from, date_to, filename)

	// Generate query
	query := fmt.Sprintf(query_template, date_from, date_to)
	log.Printf("Query: %s", query)

	return query, filename, nil
}

func getElasticConfig() (*elasticsearch.Config, error) {

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

func saveToFile(store *Store, query string, path string, filename string) error {

	time0 := time.Now().UnixMilli()
	totalHits := 0

	full_filename := path + filename + ".gz"

	// Create or open the file for writing
	fo, err := os.Create(full_filename)
	if err != nil {
		return fmt.Errorf("error creating file: %w", err)
	}
	gf := gzip.NewWriter(fo)
	fw := bufio.NewWriter(gf)

	defer func() {
		fw.Flush()
		gf.Close()
		if err := fo.Close(); err != nil {
			log.Printf("Error closing file: %s", err)
		}
	}()

	// Iterate through search results
	last_sort := ""
	var result []string

	for {
		result, last_sort, err = store.search(query, last_sort)
		totalHits += len(result)

		if err != nil {
			log.Printf("Error searching: %s", err)
			break
		}

		if len(result) == 0 {
			break
		}

		// write a chunk
		if _, err := fw.Write([]byte(strings.Join(result, "\n") + "\n")); err != nil {
			return err
		}

		if isShuttingDown.Load() {
			log.Println("Gracefully shutting down, stopping now...")
			break
		}

	}

	time1 := time.Now().UnixMilli()
	log.Printf("End of results, total hits:%d, time taken: %d seconds, output filename: %s", totalHits, (time1-time0)/1000, full_filename)

	return nil
}

func getCommandLineArgs() ArgsOptions {

	var opts ArgsOptions

	// Get args
	args, err := flags.ParseArgs(&opts, os.Args)

	// Check for errors
	switch err := err.(type) {
	case nil:
		break
	case *flags.Error:
		if err.Type == flags.ErrHelp {
			os.Exit(0)
		} else {
			os.Exit(1)
		}
	default:
		os.Exit(1)
	}

	log.Printf("Parsed flags: %+v, args: %v", opts, args)

	return opts
}

func lisenForShutdown(ctx context.Context, stop context.CancelFunc) {
	<-ctx.Done()
	log.Println("Received shutdown signal")
	isShuttingDown.Store(true)
	stop()
}
