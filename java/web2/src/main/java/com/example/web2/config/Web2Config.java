package com.example.web2.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.databind.ObjectMapper;

@Configuration
public class Web2Config {

    private static final Logger logger = LoggerFactory.getLogger(Web2Config.class);


    @Bean
    public RestTemplate restTemplate() {
        logger.info("Bean: RestTemplate was initialized");
        return new RestTemplate();
    }

    @Bean
    public ObjectMapper objectMapper() {
        logger.info("Bean: ObjectMapper was initialized");
        return new ObjectMapper();
    }

}
