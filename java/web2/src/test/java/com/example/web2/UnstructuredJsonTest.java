package com.example.web2;

import com.example.web2.Web2ApplicationTests;
import com.example.web2.config.SpringTestConfig;
import com.example.web2.model.SyslogEntry;
import com.example.web2.repository.SyslogEntryRepository;
import com.example.web2.repository.UserRepository;
import com.example.web2.service.ImportElasticService;
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
@SpringBootTest(classes = Web2Application.class)
public class UnstructuredJsonTest {
    private static final Logger logger = LoggerFactory.getLogger(UnstructuredJsonTest.class);

    @Autowired
    private ImportElasticService importElasticService;

    @Autowired
    private SyslogEntryRepository syslogEntryRepository;

    @Test
    public void unstructuredJson() throws Exception {

        String filename = "/testData/syslog.json";

        importElasticService.loadJsonFile(filename);
        var stream = importElasticService.getStream();

        stream.forEach(e -> {
            logger.info(e.toString());
            syslogEntryRepository.save(e);
        });

    }
    @Test
    public void elasticSearchTest() throws Exception {

        importElasticService.downloadSyslog();

    }




}
