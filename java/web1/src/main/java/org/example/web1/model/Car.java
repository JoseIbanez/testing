package org.example.web1.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.apache.commons.lang3.RandomStringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.invoke.MethodHandles;

import java.util.UUID;

public class Car {

    private String maker;
    @JsonProperty
    public int speed;
    @JsonProperty
    public  String plate;
    @JsonProperty
    public UUID serialNumber;

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));


    public Car() {
        this.maker = "None";
        this.plate = generate_random_plate();
        this.speed = 0;
        this.serialNumber = UUID.randomUUID();
    }

    public Car(String maker) {
        this.maker = maker;
        this.plate = generate_random_plate();
        this.speed = 0;
        this.serialNumber = UUID.randomUUID();
    }

    public Car(String maker, String plate) {
        this.maker = maker;
        this.plate = plate;
        this.speed = 0;
        this.serialNumber = UUID.randomUUID();
    }

    @Override
    public String toString(){
        return String.format("Car: Plate=%s, Marker=%s, SN=%s",
                this.plate, this.maker, this.serialNumber.toString());
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

    public void setSerialNumber(String serialNumber) {
        try {
            this.serialNumber = UUID.fromString(serialNumber);
        } catch (IllegalArgumentException err) {
            logger.error("Invalid serial number:{}, error:{}. Using a random one", serialNumber, err.toString());
            this.serialNumber = UUID.randomUUID();
        }
    }
    public String getSerialNumber() {
        return serialNumber.toString();
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
