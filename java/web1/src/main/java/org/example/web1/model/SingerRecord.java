package org.example.web1.model;


public record SingerRecord {
    public record Singer(Long id, String firstName, String LastName) { }
    public record SingerAlbum(Long id, String firstName, String LastName) {}
}