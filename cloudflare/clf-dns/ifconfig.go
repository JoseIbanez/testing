package main

import (
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"strings"
)

const defaultResolverIPURL = "https://ifconfig.me/ip"

// getMyPublicIP returns the public IP address as reported by the resolver
// provider, overridable with the RESOLVER_IP_URL environment variable.
func getMyPublicIP() (*string, error) {
	providerURL := defaultResolverIPURL
	if custom := strings.TrimSpace(os.Getenv("RESOLVER_IP_URL")); custom != "" {
		providerURL = custom
	}

	resp, err := http.Get(providerURL)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("%s: unexpected status %s", providerURL, resp.Status)
	}

	// The endpoint answers with the bare IP as plain text, not JSON.
	body, err := io.ReadAll(io.LimitReader(resp.Body, 64))
	if err != nil {
		return nil, err
	}

	ip := strings.TrimSpace(string(body))
	if net.ParseIP(ip) == nil {
		return nil, fmt.Errorf("%s: invalid IP address %q", providerURL, ip)
	}

	return &ip, nil
}
