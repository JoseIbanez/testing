package com.example.web2.service;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.query_dsl.FieldAndFormat;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import com.example.web2.model.SyslogEntryES;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import jakarta.json.Json;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.List;
import java.util.Spliterator;
import java.util.Spliterators;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

import com.example.web2.model.SyslogEntry;

@Service
public class ImportElasticService {

    private static final Logger logger = LoggerFactory.getLogger(ImportElasticService.class);

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private Environment env;

    @Autowired
    private ElasticsearchClient elasticsearchClient;

    private String filename = "/testData/syslog.json";
    private JsonNode input;

    public void loadJsonFile(String fileName)  {

        this.filename = fileName;
        var fileStream = this.getClass().getResourceAsStream(filename);

        logger.info("Read file:{}",fileName);
        input = objectMapper.createObjectNode();

        try {
            input = objectMapper.readTree(fileStream);

        } catch (IOException err) {
            logger.error("File {}, error:{}",fileName,err.toString());
            input = objectMapper.createObjectNode();
        }


    }

    public Stream<SyslogEntry> getStream() {

        JsonNode hits = input.at("/hits/hits");

        Stream<SyslogEntry> stream = StreamSupport.stream(
                        Spliterators.spliteratorUnknownSize(hits.iterator(),
                                Spliterator.ORDERED | Spliterator.IMMUTABLE | Spliterator.CONCURRENT), true)
                .map(hit -> new SyslogEntry(
                        hit.at("/fields/device_name/0").asText(),
                        hit.at("/fields/tenant_name/0").asText(),
                        hit.at("/fields/syslog-timestamp/0").asText(),
                        hit.at("/fields/message/0").asText()
                ))
                .peek(event -> logger.info(event.getTimestamp()));

        return stream;

    }


    public String downloadSyslog() throws IOException {

        SearchResponse<ObjectNode> response = elasticsearchClient.search(s -> s
                .index("rn*syslog*")
                        .query(q -> q
                        .match(t-> t
                                .field("tenant_name")
                                .query("CPS"))
                        ).size(1000)
                ,ObjectNode.class);

        logger.info(response.toString());

        for (Hit<ObjectNode> hit: response.hits().hits()) {
            if (hit.source() == null) continue;
            ObjectNode source = hit.source();
            logger.info(source.get("device_name").toString());
            logger.info(source.get("tenant_name").toString());
        }


        return "hi";
    }



}
