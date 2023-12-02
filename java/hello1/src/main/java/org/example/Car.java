package org.example;
import org.apache.commons.lang3.RandomStringUtils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.lang.invoke.MethodHandles;
import java.util.Locale;

public class Car {

    private String maker;
    public int speed;
    public  String plate;

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));


    public Car() {}

    public Car(String maker) {
        this.maker = maker;
        this.plate = generate_random_plate();
        this.speed = 0;
    }

    public Car(String maker, String plate) {
        this.maker = maker;
        this.plate = plate;
        this.speed = 0;
    }

    @Override
    public String toString(){
        return String.format("Car: Plate=%s, Marker=%s", this.plate, this.maker);
    }

    public int getSpeed() {
        return speed;
    }

    public void setSpeed(int speed) {
        this.speed = speed;
    }

    public String getMaker() {
        return maker;
    }

    public void setMaker(String maker) {
        this.maker = maker;
    }



    private static String generate_random_plate() {
        String new_plate = String.format("%s%s",
                RandomStringUtils.randomNumeric(4),
                RandomStringUtils.randomAlphabetic(3).toUpperCase()
        );
        logger.debug("New plate was generated: {}",new_plate);
        return new_plate;
    }


}
