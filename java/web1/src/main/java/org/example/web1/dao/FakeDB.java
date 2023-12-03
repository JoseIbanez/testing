package org.example.web1.dao;


import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.invoke.MethodHandles;
import java.util.Optional;
import java.util.UUID;

import org.example.web1.model.Car;
import org.springframework.stereotype.Repository;


@Repository("fakeDao")
public class FakeDB implements CarDao {

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));
    private static List<Car> CarDB = new ArrayList<Car>();

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
            return -1;
        }
        testCar = selectCarByPlate(car.plate);
        if (testCar.isPresent()) {
            logger.error("Duplicated plate:{}",car.plate);
            return -1;
        }

        logger.info("Saving... {}",car);
        CarDB.add(car);
        return 0;
    }




}
