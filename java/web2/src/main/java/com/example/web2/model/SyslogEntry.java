package com.example.web2.model;

import jakarta.persistence.*;

import java.util.Objects;


@Entity
@Table(name = "syslog")
public class SyslogEntry {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "syslog_generator")
    @SequenceGenerator(name = "syslog_generator", sequenceName = "syslog_id_seq", allocationSize = 1)
    private Long id;

    private String deviceName;
    private String tenantName;
    private String timestamp;
    private String message;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getDeviceName() {
        return deviceName;
    }

    public void setDeviceName(String deviceName) {
        this.deviceName = deviceName;
    }

    public String getTenantName() {
        return tenantName;
    }

    public void setTenantName(String tenantName) {
        this.tenantName = tenantName;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public SyslogEntry() {
    }

    public SyslogEntry(String deviceName, String tenantName, String timestamp, String message) {
        this.id = (long) hashCode();
        this.deviceName = deviceName;
        this.tenantName = tenantName;
        this.timestamp = timestamp;
        this.message = message;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        SyslogEntry that = (SyslogEntry) o;

        if (!Objects.equals(id, that.id)) return false;
        if (!Objects.equals(deviceName, that.deviceName)) return false;
        if (!Objects.equals(tenantName, that.tenantName)) return false;
        if (!Objects.equals(timestamp, that.timestamp)) return false;
        return Objects.equals(message, that.message);
    }

    @Override
    public int hashCode() {
        return Objects.hash(deviceName, tenantName, timestamp, message);
    }

    @Override
    public String toString() {
        return String.format("timestamp:%s deviceName:%s, message:%s",timestamp,deviceName,message);
    }


}