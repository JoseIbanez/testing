package com.example.web2;

import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.assertEquals;

import com.example.web2.model.SyslogEntry;
import com.example.web2.repository.SyslogEntryRepository;




@SpringBootTest(classes = Web2Application.class)
class SyslogEntryRepositoryTest {

    private static final Logger logger = LoggerFactory.getLogger(SyslogEntryRepositoryTest.class);


    @Autowired
    private SyslogEntryRepository syslogEntryRepository;

    @Test
    void setSyslogEntryRepositoryTest() {

        SyslogEntry entry = new SyslogEntry("VF0001-10001", "VGE", "Dec 28 08:08:08", "Hi There");

        SyslogEntry savedEntry = syslogEntryRepository.save(entry);

        assertEquals(savedEntry,entry);

    }


}
