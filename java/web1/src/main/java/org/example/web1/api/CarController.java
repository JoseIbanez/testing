package org.example.web1.api;

import java.lang.invoke.MethodHandles;
import java.util.List;
import java.util.Optional;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import org.example.web1.model.Car;
import org.example.web1.service.CarService;
import org.springframework.web.server.ResponseStatusException;


@RequestMapping("api/v1/car")
@RestController
public class CarController {

    private final CarService carService;
    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));

    @Autowired
    public CarController(CarService carService) {
        this.carService = carService;
    }

    @PostMapping
    public Car updateCar(@RequestBody Car car) {
        logger.info("new {}",car);
        var result = carService.updateCar(car);
        if (result <0 ) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Duplicated car");
        }

        return car;
    }

    @GetMapping
    public List<Car> selectAllCars() {
        return carService.selectAllCars();
    }

    @GetMapping(path = "{id}")
    public Optional<Car> selectCarById(@PathVariable("id") String id) {
        logger.info("Search car id:{}",id);
        return carService.selectCarById(id);
    }

}



