package org.example;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.MockitoAnnotations;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.invoke.MethodHandles;

import static org.mockito.Mockito.when;

public class TestClassB {

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));


    @InjectMocks
    ClassB b;

    @Spy
    ClassA a;

    @BeforeEach
    public void init() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testCounter() {

        logger.info("Begin");

        logger.info("Mocks");
        when(a.getBody()).thenReturn("a a a b b b a");

        logger.info("Test");
        b.analize();
        int count = b.getCounter();

        logger.info("Assertions");
        Assertions.assertEquals(count,7);

        logger.info("Done");

    }

}
