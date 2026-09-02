package main

import (
	"os"
	"strings"
	"testing"
)

func TestGetZonesInfo(t *testing.T) {
	if os.Getenv("CLOUDFLARE_API_TOKEN") == "" {
		t.Skip("CLOUDFLARE_API_TOKEN not set")
	}

	zones, err := getZonesInfo()
	if err != nil {
		t.Fatal(err)
	}

	for _, zone := range zones {
		t.Logf("zone: id=%s name=%s", zone.ID, zone.Name)
	}
}

func TestGetDNSRecordsEmptyZoneID(t *testing.T) {
	if _, err := getDNSRecords(""); err == nil {
		t.Fatal("expected an error for an empty zone ID")
	}
}

func TestGetDNSRecords(t *testing.T) {
	if os.Getenv("CLOUDFLARE_API_TOKEN") == "" {
		t.Skip("CLOUDFLARE_API_TOKEN not set")
	}

	zones, err := getZonesInfo()
	if err != nil {
		t.Fatal(err)
	}
	if len(zones) == 0 {
		t.Skip("no zones available for the configured token")
	}

	records, err := getDNSRecords(zones[0].ID)
	if err != nil {
		t.Fatal(err)
	}

	for _, record := range records {
		t.Logf("record: id=%s type=%s name=%s content=%s", record.ID, record.Type, record.Name, record.Content)
	}
}

func TestSetDNSRecordsValidation(t *testing.T) {
	valid := DNSRecord{ID: "rec", Type: "A", Name: "test.example.com", Content: "127.0.0.1"}

	cases := []struct {
		name   string
		zoneID string
		record DNSRecord
	}{
		{"empty zone ID", "", valid},
		{"empty record ID", "zone", DNSRecord{Type: "A", Name: valid.Name, Content: valid.Content}},
		{"empty type", "zone", DNSRecord{ID: valid.ID, Name: valid.Name, Content: valid.Content}},
		{"empty name", "zone", DNSRecord{ID: valid.ID, Type: valid.Type, Content: valid.Content}},
		{"empty content", "zone", DNSRecord{ID: valid.ID, Type: valid.Type, Name: valid.Name}},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			if _, err := setDNSRecords(tc.zoneID, tc.record); err == nil {
				t.Fatalf("expected an error for %s", tc.name)
			}
		})
	}
}

func TestSetDNSRecords(t *testing.T) {
	if os.Getenv("CLOUDFLARE_API_TOKEN") == "" {
		t.Skip("CLOUDFLARE_API_TOKEN not set")
	}

	targetEntry := "manual1.lunes.ovh"

	zones, err := getZonesInfo()
	if err != nil {
		t.Fatal(err)
	}

	var zoneID string
	for _, zone := range zones {
		if targetEntry == zone.Name || strings.HasSuffix(targetEntry, "."+zone.Name) {
			zoneID = zone.ID
			break
		}
	}
	if zoneID == "" {
		t.Skipf("no zone matching %s available for the configured token", targetEntry)
	}

	records, err := getDNSRecords(zoneID)
	if err != nil {
		t.Fatal(err)
	}

	var target *DNSRecord
	for i, record := range records {
		if record.Name == targetEntry {
			target = &records[i]
			break
		}
	}
	if target == nil {
		t.Skipf("no record named %s in zone %s", targetEntry, zoneID)
	}
	t.Logf("using zone=%s record=%s name=%s content=%s", zoneID, target.ID, target.Name, target.Content)

	// Re-applies the current values so the update stays a no-op against the live zone.
	updated, err := setDNSRecords(zoneID, *target)
	if err != nil {
		t.Fatal(err)
	}

	if updated.ID != target.ID {
		t.Fatalf("expected record ID %s, got %s", target.ID, updated.ID)
	}
	if updated.Content != target.Content {
		t.Fatalf("expected content %s, got %s", target.Content, updated.Content)
	}
	t.Logf("updated: id=%s type=%s name=%s content=%s", updated.ID, updated.Type, updated.Name, updated.Content)
}

func TestGetDNSRecordByNameEmptyName(t *testing.T) {
	if _, err := getDNSRecordByName(""); err == nil {
		t.Fatal("expected an error for an empty record name")
	}
}

func TestGetDNSRecordByName(t *testing.T) {
	if os.Getenv("CLOUDFLARE_API_TOKEN") == "" {
		t.Skip("CLOUDFLARE_API_TOKEN not set")
	}

	targetEntry := "manual1.lunes.ovh"

	record, err := getDNSRecordByName(targetEntry)
	if err != nil {
		t.Fatal(err)
	}

	if record.Name != targetEntry {
		t.Fatalf("expected record name %s, got %s", targetEntry, record.Name)
	}
	t.Logf("record: id=%s type=%s name=%s content=%s", record.ID, record.Type, record.Name, record.Content)
}

func TestGetDNSRecordByNameUnknown(t *testing.T) {
	if os.Getenv("CLOUDFLARE_API_TOKEN") == "" {
		t.Skip("CLOUDFLARE_API_TOKEN not set")
	}

	if _, err := getDNSRecordByName("does-not-exist.invalid"); err == nil {
		t.Fatal("expected an error for a name outside any zone")
	}
}
