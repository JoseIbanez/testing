package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strings"
)

const apiBaseURL = "https://api.cloudflare.com/client/v4"

type CloudflareConfig struct{
	APIKey string
}

type ZoneInfo struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type DNSRecord struct {
	ID      string `json:"id"`
	ZoneID  string `json:"zone_id"`
	Type    string `json:"type"`
	Name    string `json:"name"`
	Content string `json:"content"`
}

// getCloudflareConfig builds the Cloudflare configuration from the
// CLOUDFLARE_API_TOKEN environment variable.
func getCloudflareConfig() (*CloudflareConfig, error) {
	apiKey, ok := os.LookupEnv("CLOUDFLARE_API_TOKEN")
	if !ok || apiKey == "" {
		return nil, fmt.Errorf("CLOUDFLARE_API_TOKEN environment variable is not set")
	}

	return &CloudflareConfig{
		APIKey: apiKey,
	}, nil
}


// getZonesInfo retrieves the list of zones from Cloudflare.
func getZonesInfo() ([]ZoneInfo, error) {
	config, err := getCloudflareConfig()
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest(http.MethodGet, apiBaseURL+"/zones", nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+config.APIKey)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("cloudflare: unexpected status %s", resp.Status)
	}

	var body struct {
		Success bool       `json:"success"`
		Result  []ZoneInfo `json:"result"`
		Errors  []struct {
			Code    int    `json:"code"`
			Message string `json:"message"`
		} `json:"errors"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
		return nil, err
	}
	if !body.Success {
		if len(body.Errors) > 0 {
			return nil, fmt.Errorf("cloudflare: %d %s", body.Errors[0].Code, body.Errors[0].Message)
		}
		return nil, fmt.Errorf("cloudflare: request failed")
	}

	return body.Result, nil
}



// getDNSRecords retrieves the list of DNS records for a given zone from Cloudflare
func getDNSRecords(zoneID string) ([]DNSRecord, error) {
	if zoneID == "" {
		return nil, fmt.Errorf("cloudflare: zone ID is required")
	}

	config, err := getCloudflareConfig()
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest(http.MethodGet, apiBaseURL+"/zones/"+url.PathEscape(zoneID)+"/dns_records", nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+config.APIKey)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("cloudflare: unexpected status %s", resp.Status)
	}

	var body struct {
		Success bool        `json:"success"`
		Result  []DNSRecord `json:"result"`
		Errors  []struct {
			Code    int    `json:"code"`
			Message string `json:"message"`
		} `json:"errors"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
		return nil, err
	}
	if !body.Success {
		if len(body.Errors) > 0 {
			return nil, fmt.Errorf("cloudflare: %d %s", body.Errors[0].Code, body.Errors[0].Message)
		}
		return nil, fmt.Errorf("cloudflare: request failed")
	}

	return body.Result, nil
}


// update a DNS record for a given zone in Cloudflare.
func setDNSRecords(zoneID string, record DNSRecord) (*DNSRecord, error) {
	if zoneID == "" {
		return nil, fmt.Errorf("cloudflare: zone ID is required")
	}
	if record.ID == "" {
		return nil, fmt.Errorf("cloudflare: record ID is required")
	}
	if record.Type == "" || record.Name == "" || record.Content == "" {
		return nil, fmt.Errorf("cloudflare: record type, name and content are required")
	}

	config, err := getCloudflareConfig()
	if err != nil {
		return nil, err
	}

	payload, err := json.Marshal(struct {
		Type    string `json:"type"`
		Name    string `json:"name"`
		Content string `json:"content"`
	}{
		Type:    record.Type,
		Name:    record.Name,
		Content: record.Content,
	})
	if err != nil {
		return nil, err
	}

	endpoint := apiBaseURL + "/zones/" + url.PathEscape(zoneID) + "/dns_records/" + url.PathEscape(record.ID)
	req, err := http.NewRequest(http.MethodPatch, endpoint, bytes.NewReader(payload))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+config.APIKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("cloudflare: unexpected status %s", resp.Status)
	}

	var body struct {
		Success bool      `json:"success"`
		Result  DNSRecord `json:"result"`
		Errors  []struct {
			Code    int    `json:"code"`
			Message string `json:"message"`
		} `json:"errors"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
		return nil, err
	}
	if !body.Success {
		if len(body.Errors) > 0 {
			return nil, fmt.Errorf("cloudflare: %d %s", body.Errors[0].Code, body.Errors[0].Message)
		}
		return nil, fmt.Errorf("cloudflare: request failed")
	}

	return &body.Result, nil
}



// getDNSRecordByName 
// uses previous functions to retrive the specific DNS record by its name from Cloudflare.
func getDNSRecordByName(name string) (*DNSRecord, error) {
	if name == "" {
		return nil, fmt.Errorf("cloudflare: record name is required")
	}

	zones, err := getZonesInfo()
	if err != nil {
		return nil, err
	}

	// Picks the longest matching zone so subdomain delegations win over the apex.
	var zoneID string
	var zoneName string
	for _, zone := range zones {
		if name != zone.Name && !strings.HasSuffix(name, "."+zone.Name) {
			continue
		}
		if len(zone.Name) > len(zoneName) {
			zoneID = zone.ID
			zoneName = zone.Name
		}
	}
	if zoneID == "" {
		return nil, fmt.Errorf("cloudflare: no zone found for record %q", name)
	}

	records, err := getDNSRecords(zoneID)
	if err != nil {
		return nil, err
	}

	for i, record := range records {
		if record.Name == name {
			// The list endpoint omits zone_id, so fill it in from the matched zone.
			records[i].ZoneID = zoneID
			return &records[i], nil
		}
	}

	return nil, fmt.Errorf("cloudflare: record %q not found in zone %s", name, zoneName)
}