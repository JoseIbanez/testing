package org.example.web1.db;

import org.example.web1.repo.SingerRepo;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.jdbc.Sql;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@ActiveProfiles("test")
@Sql({ "classpath:h2/create-schema.sql","classpath:h2/test-data.sql" })
@SpringBootTest
public class JdbcTemplateTest {
    private static Logger LOGGER = LoggerFactory.getLogger(JdbcTemplateTest.class);

    @Autowired
    SingerRepo singerRepo;

    @Test
    public void test01() throws Exception {

        var name = singerRepo.findNameById(1);
        LOGGER.info("name:{}",name.toString());
    }


}