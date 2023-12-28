package com.example.web2.model;

public record SyslogEntryES(String device_name, String tenant_name, String syslog_timestamp, String message) { }

