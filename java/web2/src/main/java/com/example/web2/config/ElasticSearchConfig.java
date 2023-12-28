package com.example.web2.config;

import org.apache.catalina.authenticator.BasicAuthenticator;
import org.apache.http.Header;
import org.apache.http.HttpHost;
import org.apache.http.message.BasicHeader;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.ElasticsearchTransport;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.elasticsearch.client.RestClient;

import java.nio.charset.StandardCharsets;
import java.util.Base64;

@Configuration
public class ElasticSearchConfig {

    private static final Logger logger = LoggerFactory.getLogger(ElasticSearchConfig.class);

    @Autowired
    private Environment env;


    @Bean
    public ElasticsearchClient elasticsearchClient() {

        // URL and Auth key
        String serverUrl =  env.getProperty("app.elasticsearch.url");
        String authKey = Base64.getEncoder().withoutPadding().encodeToString(
                String.format("%s:%s",
                                env.getProperty("app.elasticsearch.username"),
                                env.getProperty("app.elasticsearch.password"))
                        .getBytes(StandardCharsets.UTF_8)
        );


        // Create the low-level client
        RestClient restClient = RestClient
                .builder(HttpHost.create(serverUrl))
                .setDefaultHeaders(new Header[]{
                        new BasicHeader("Authorization", "Basic " + authKey),
                })
                .build();

        // Create the transport with a Jackson mapper
        ElasticsearchTransport transport = new RestClientTransport(
                restClient, new JacksonJsonpMapper());

        return new ElasticsearchClient(transport);

    }

}
