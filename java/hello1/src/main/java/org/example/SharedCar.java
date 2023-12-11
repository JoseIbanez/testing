package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.invoke.MethodHandles;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class SharedCar extends Car {

    private final Lock lock = new ReentrantLock();
    private Optional<String> driver;
    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));

    public SharedCar(String maker) {
        super(maker);
        this.driver = Optional.empty();
    }


    public Optional<String> getDriver() {
        return driver;
    }

    public void lock() {
        lock.lock();
    }

    public void unlock() {
        lock.unlock();
    }

    public boolean tryLock(long millis) {

        try {
            return lock.tryLock(millis, TimeUnit.MILLISECONDS);
        } catch(InterruptedException err ) {
            return false;
        }

    }


    public void setDriver(String driver) {
        logger.info("Car:{} driven by:{}",this.plate,driver);
        this.driver = Optional.of(driver);
    }

    public void unsetDriver() {
        logger.info("Car:{} is free",this.plate);
        this.driver = Optional.empty();
    }


}
