package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.invoke.MethodHandles;
import java.util.List;

public class ClassB {

    private int counter;
    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));


    private ClassA a;


    public ClassB() {
        counter = 0;
        a = new ClassA();
    }


    public int analize() {

        a.loadBody();

        var body = a.getBody();
        logger.info("Test: {}",body);

        String[] words = body.split(" ");
        counter = words.length;

        return counter;

    }


    public int getCounter() {
        return counter;
    }

    public void setCounter(int counter) {
        this.counter = counter;
    }
}
