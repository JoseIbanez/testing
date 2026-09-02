package main

import (
	"flag"
	"fmt"
	"log"
)

func main() {
	name := flag.String("name", "", "DNS record name to check and update")
	dryRun := flag.Bool("dry-run", false, "report the change without applying it")
	flag.Parse()

	if *name == "" {
		flag.Usage()
		log.Fatal("-name is required")
	}

	record, err := getDNSRecordByName(*name)
	if err != nil {
		log.Fatal(err)
	}

	ip, err := getMyPublicIP()
	if err != nil {
		log.Fatal(err)
	}

	if record.Content == *ip {
		fmt.Printf("%s already points to %s\n", record.Name, *ip)
		return
	}

	if *dryRun {
		fmt.Printf("dry-run: would update %s from %s to %s\n", record.Name, record.Content, *ip)
		return
	}

	if record.ZoneID == "" {
		log.Fatalf("cloudflare: no zone ID returned for record %s", record.Name)
	}

	record.Content = *ip
	updated, err := setDNSRecords(record.ZoneID, *record)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("updated %s to %s\n", updated.Name, updated.Content)
}
