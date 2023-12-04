package org.example.web1.dao;


import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.invoke.MethodHandles;
import java.util.Optional;
import java.util.UUID;

import org.example.web1.model.Car;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Repository;
import org.springframework.web.server.ResponseStatusException;


@Repository("fakeDao")
public class FakeDB implements CarDao {

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));
    private static List<Car> CarDB = new ArrayList<Car>();
    private static int buffer_counter = 0;

    @Override
    public List<Car> selectAllCars() {
        logger.info("Query for all cars");
        return CarDB;
    }

    @Override
    public Optional<Car> selectCarBySerialNumber(String serialNumber) {
        try {
            UUID realSerialNumber = UUID.fromString(serialNumber);
            return selectCarBySerialNumber(realSerialNumber);

        } catch (IllegalArgumentException err) {
            logger.error("Invalid serial number:{}, error:{}. Using a random one", serialNumber, err.toString());
            return Optional.empty();
        }

    }

    @Override
    public Optional<Car> selectCarBySerialNumber(UUID serialNumber) {
        Optional<Car> resultCar = CarDB.stream()
                .filter(car -> car.serialNumber.equals(serialNumber))
                .findFirst();

        if (resultCar.isPresent()) {
            logger.info("Found car for SN:{} -> {}",serialNumber,resultCar.get());
        } else {
            logger.info("Car not found for SN:{}",serialNumber);
        }

        return resultCar;
    }

    @Override
    public Optional<Car> selectCarByPlate(String plate) {
        Optional<Car> resultCar = CarDB.stream()
                .filter(car -> car.plate.equals(plate))
                .findFirst();

        if (resultCar.isPresent()) {
            logger.info("Found car for Plate:{} -> {}",plate,resultCar.get());
        } else {
            logger.info("Car not found for Plate:{}",plate);
        }

        return resultCar;
    }

    @Override
    public int updateCar(Car car) {

        Optional<Car> testCar;

        testCar = selectCarBySerialNumber(car.serialNumber);
        if (testCar.isPresent()) {
            logger.error("Duplicated serialNumber:{}",car.serialNumber);
            //return -1;
            throw new RuntimeException("Duplicated SerialNumber");
            //throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Duplicated SerialNumber");
        }
        testCar = selectCarByPlate(car.plate);
        if (testCar.isPresent()) {
            logger.error("Duplicated plate:{}",car.plate);
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Duplicated Plate");
            //return -1;
        }

        logger.info("Saving... {}",car);
        CarDB.add(car);

        if (buffer_counter++ > 5) {
            buffer_counter =0;
            saveToFile();
        }


        return 0;
    }


    public int saveToFile() {

        try {
            ObjectMapper objectMapper = new ObjectMapper();

            objectMapper.writeValue(new File("/tmp/car_db.json"), CarDB);
            logger.info("DB saved, Items:{}", CarDB.size());
            return 0;

        } catch (IOException e) {
            logger.error(e.toString());
            return -1;
        }

    }

    public int loadFromFile() {

        try {
            ObjectMapper objectMapper = new ObjectMapper();

            //String jsonString = objectMapper.writeValueAsString(CarDB);
            //logger.info("DB: {}", jsonString);
            CarDB = objectMapper.readValue(new File("/tmp/car_db.json"), new TypeReference<List<Car>>() {});
            logger.info("DB loaded, Items:{}", CarDB.size());
            return 0;

        } catch (IOException e) {
            logger.error(e.toString());
            return -1;
        }

    }



}
