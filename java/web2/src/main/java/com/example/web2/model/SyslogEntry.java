package com.example.web2.model;

public record SyslogEntry(String deviceName, String tenantName, String timestamp, String message) {}

