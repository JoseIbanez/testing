package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGetMyPublicIPCustomProvider(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("203.0.113.7\n"))
	}))
	defer server.Close()

	t.Setenv("RESOLVER_IP_URL", server.URL)

	ip, err := getMyPublicIP()
	if err != nil {
		t.Fatal(err)
	}
	if *ip != "203.0.113.7" {
		t.Fatalf("expected 203.0.113.7, got %s", *ip)
	}
}

func TestGetMyPublicIPInvalidBody(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("not-an-ip"))
	}))
	defer server.Close()

	t.Setenv("RESOLVER_IP_URL", server.URL)

	if _, err := getMyPublicIP(); err == nil {
		t.Fatal("expected an error for a non-IP response")
	}
}

func TestGetMyPublicIPUnexpectedStatus(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.Error(w, "boom", http.StatusInternalServerError)
	}))
	defer server.Close()

	t.Setenv("RESOLVER_IP_URL", server.URL)

	if _, err := getMyPublicIP(); err == nil {
		t.Fatal("expected an error for a non-200 status")
	}
}

func TestGetMyPublicIPDefaultProvider(t *testing.T) {
	t.Setenv("RESOLVER_IP_URL", "")

	ip, err := getMyPublicIP()
	if err != nil {
		t.Skipf("default provider unreachable: %v", err)
	}

	t.Logf("public IP: %s", *ip)
}
