package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.invoke.MethodHandles;

public class ClassA {

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));


    private String body;

    public ClassA() {
    }

    public int loadBody(){
        body = "Original String";
        logger.info("Original method: loadBody, text:{}",body);
        return 0;
    }

    public String getBody() {
        logger.info("Original method: getBody, text:{}",body);
        return body;
    }

    public void setBody(String body) {
        this.body = body;
    }
}
