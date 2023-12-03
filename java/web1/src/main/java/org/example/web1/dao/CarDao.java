package org.example.web1.dao;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.example.web1.model.Car;

public interface CarDao {

    int updateCar(Car car);

    List<Car> selectAllCars();

    Optional<Car> selectCarBySerialNumber(UUID serialNumber);
    Optional<Car> selectCarBySerialNumber(String serialNumber);
    Optional<Car> selectCarByPlate(String plate);

}
