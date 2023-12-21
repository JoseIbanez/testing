package org.example.web1.db;

import org.example.web1.repo.SingerJdbcRepo;
import org.example.web1.repo.SingerRepo;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.jdbc.Sql;

import javax.sql.DataSource;
import java.sql.SQLException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@ActiveProfiles("dev")
@Sql({ "classpath:h2/create-schema.sql","classpath:h2/test-data.sql" })
@SpringBootTest
public class DataSourceConfigTest {
    private static Logger LOGGER = LoggerFactory.getLogger(DataSourceConfigTest.class);

    @Autowired
    SingerRepo singerRepo;

    @Test
    public void test01() throws Exception {

        var name = singerRepo.findNameById(1);
        LOGGER.info("name:{}",name.toString());
    }


}