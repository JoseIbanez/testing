package org.example.web1.service;

import org.example.web1.dao.CarDao;
import org.example.web1.model.Car;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import java.lang.invoke.MethodHandles;
import java.util.List;
import java.util.Optional;

@Service
public class CarService {

    private final CarDao carDao;
    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));

    @Autowired
    public CarService(@Qualifier("fakeDao") CarDao carDao) {
        logger.info("Service loading...");
        this.carDao = carDao;
    }

    public int updateCar(Car car) {
        return carDao.updateCar(car);
    }

    public List<Car> selectAllCars() {
        return carDao.selectAllCars();
    }

    public Optional<Car> selectCarById(String id){

        var resultCar = carDao.selectCarByPlate(id);

        if (resultCar.isEmpty()) {
            resultCar = carDao.selectCarBySerialNumber(id);
        }

        return resultCar;
    }

}
