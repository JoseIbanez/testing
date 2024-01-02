package com.example.web2.model;


import org.springframework.data.redis.core.RedisHash;

@RedisHash("User")
public record UserRedisEntry(String id, String name) {}

