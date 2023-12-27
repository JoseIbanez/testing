package com.example.web2;

import com.example.web2.Web2ApplicationTests;
import com.example.web2.config.SpringTestConfig;
import com.example.web2.model.SyslogEntry;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.Spliterator;
import java.util.Spliterators;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = SpringTestConfig.class)
public class UnstructuredJsonTest {
    private static final Logger logger = LoggerFactory.getLogger(UnstructuredJsonTest.class);

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void unstructuredJson() throws Exception {

        String filename = "/testData/syslog.json";

        var fileStream = this.getClass().getResourceAsStream(filename);
        JsonNode input = objectMapper.readTree(fileStream);
        JsonNode hits =  input.at("/hits/hits");


        for ( var hit: hits ) {

            String message = hit.at("/fields/message/0").asText();
            String deviceName = hit.at("/fields/device_name/0").asText();
            String timestamp = hit.at("/fields/syslog-timestamp/0").asText();
            String tenantName = hit.at("/fields/tenant_name/0").asText();

            SyslogEntry entry = new SyslogEntry(deviceName, tenantName, timestamp, message);

            logger.info(entry.toString());


        }



    }

    @Test
    public void unstructuredJson02() throws Exception {

        String filename = "/testData/syslog.json";

        var fileStream = this.getClass().getResourceAsStream(filename);
        JsonNode input = objectMapper.readTree(fileStream);
        JsonNode hits =  input.at("/hits/hits");


        Stream<SyslogEntry> stream = StreamSupport.stream(
                Spliterators.spliteratorUnknownSize(hits.iterator(),
                        Spliterator.ORDERED | Spliterator.IMMUTABLE | Spliterator.CONCURRENT),true)
                .map(hit -> new SyslogEntry(
                         hit.at("/fields/message/0").asText(),
                         hit.at("/fields/device_name/0").asText(),
                         hit.at("/fields/syslog-timestamp/0").asText(),
                         hit.at("/fields/tenant_name/0").asText()
                ))
                .peek(event -> logger.info(event.timestamp()));

        stream.forEach(e -> logger.info(e.toString()));

    }




}
