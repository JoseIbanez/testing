package com.example.web2.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisClusterConfiguration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.RedisStandaloneConfiguration;
import org.springframework.data.redis.connection.jedis.JedisClientConfiguration;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.integration.redis.util.RedisLockRegistry;
import org.springframework.integration.support.locks.ExpirableLockRegistry;

import java.time.Duration;
import java.util.Collections;

@Configuration
public class RedisConfig {


    private static final Logger logger = LoggerFactory.getLogger(com.example.web2.config.ElasticSearchConfig.class);

    private static final String LOCK_REGISTRY_REDIS_KEY = "MY_REDIS_KEY";
    private static final Duration RELEASE_TIME_DURATION = Duration.ofSeconds(10);

    @Bean
    JedisConnectionFactory jedisConnectionFactory() {
        return new JedisConnectionFactory();
    }

    @Bean
    public RedisTemplate<String, Object> redisTemplate() {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(jedisConnectionFactory());
        return template;
    }

    @Bean("LOCK_REGISTRY_BEAN")
    public ExpirableLockRegistry lockRegistry(RedisConnectionFactory redisConnectionFactory) {
        RedisLockRegistry redisLockRegistry = new RedisLockRegistry(redisConnectionFactory,
                LOCK_REGISTRY_REDIS_KEY,
                RELEASE_TIME_DURATION.toMillis());
        return redisLockRegistry;

    }
}