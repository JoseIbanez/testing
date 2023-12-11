package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.invoke.MethodHandles;
import java.util.List;
import java.util.Optional;
import java.util.Random;
import java.util.TreeMap;

public class Driver implements Runnable {

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));

    private String name;
    private int rides = 0;
    private List<SharedCar> carList;
    private Optional<String> currentCar;

    public Driver(String name, List<SharedCar> carList) {
        this.name = name;
        this.carList = carList;
        this.currentCar = Optional.empty();
    }

    public void run() {

        SharedCar car;
        int numberCars = carList.size();
        Random index = new Random();

        for (int i = 0; i < 500; i++) {

            try {
                Thread.sleep(100);


                car = carList.get(index.nextInt(numberCars));

                if (car.tryLock(10)) {
                    car.setDriver(name);
                    car.setSpeed(100);

                    rides++;
                    logger.info("Driver:{}, round {}, with Car{}, rides:{}",name,i,car.plate,rides);
                    Thread.sleep(2000);


                    car.unsetDriver();
                    car.setSpeed(0);
                    car.unlock();
                }




            } catch (InterruptedException err) {
                logger.error(err.toString());
            }


        }


    }

}

