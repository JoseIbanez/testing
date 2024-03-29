package com.example.web2.service;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.SearchStats;
import co.elastic.clients.elasticsearch._types.query_dsl.FieldAndFormat;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.json.JsonpMapper;
import com.example.web2.model.SyslogEntryES;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import jakarta.json.Json;
import jakarta.json.stream.JsonGenerator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import java.io.*;
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

    public void saveTrace(Object object) throws IOException {

        FileOutputStream file = new FileOutputStream("/tmp/trace.ser");
        ObjectOutputStream out = new ObjectOutputStream(file);

        out.writeObject(object);
        out.close();
        file.close();
    }

    public Stream<SyslogEntry> downloadSyslog(String tenant_name) throws IOException {

        SearchResponse<ObjectNode> response = elasticsearchClient.search(s -> s
                .index("rn*syslog*")
                        .query(q -> q
                        .match(t-> t
                                .field("tenant_name")
                                .query(tenant_name))
                        ).size(50)
                ,ObjectNode.class);



        List<Hit<ObjectNode>> hits = response.hits().hits();
        Stream<SyslogEntry> stream = StreamSupport.stream(
                        Spliterators.spliteratorUnknownSize(hits.iterator(),
                                Spliterator.ORDERED | Spliterator.IMMUTABLE | Spliterator.CONCURRENT), false)
                .map(hit -> hit.source())
                .filter(source ->  source != null )
                .map(source -> new SyslogEntry(
                        source.get("device_name").asText(),
                        source.get("tenant_name").asText(),
                        source.get("syslog-timestamp").asText(),
                        source.get("message").asText()
                ))
                .peek(event -> logger.info(event.getTimestamp()));

        return stream;

    }

    public void justDownloadSyslog(String tenant_name) throws IOException {

        SearchResponse<ObjectNode> response = elasticsearchClient.search(s -> s
                        .index("rn*syslog*")
                        .query(q -> q
                                .match(t -> t
                                        .field("tenant_name")
                                        .query("CPS"))
                        )
                        .fields(FieldAndFormat.of( ff -> ff.field("tenant_name")))
                        .fields(FieldAndFormat.of( ff -> ff.field("device_name")))
                        .fields(FieldAndFormat.of( ff -> ff.field("syslog-timestamp")))
                        .fields(FieldAndFormat.of( ff -> ff.field("message")))
                        .storedFields("tenant_name","device_name","syslog-timestamp","message")
                        .size(10000)
                , ObjectNode.class);



        JsonpMapper mapper = elasticsearchClient._jsonpMapper();
        StringWriter writer = new StringWriter();
        JsonGenerator generator = mapper.jsonProvider().createGenerator(writer);
        mapper.serialize(response, generator);
        generator.close();
        writer.close();

        String responseString = writer.toString();
        logger.info("Response, len:{}",responseString.length());

        input = objectMapper.readTree(responseString);

    }


    }
