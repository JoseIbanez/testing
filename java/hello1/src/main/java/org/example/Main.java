package org.example;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import java.util.ArrayList;
import java.util.List;


// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
public class Main {

    static Logger logger = LogManager.getLogger(Main.class);


    public static void main(String[] args) {
        // Press Opt+Enter with your caret at the highlighted text to see how
        // IntelliJ IDEA suggests fixing it.
        System.out.printf("Hello and welcome to %s!\n","java");

        int x;
        Car car1 = new Car("Tesla");
        Car car2 = new Car("BMW","0001BBD");

        logger.info("This {} is nice.",car1.toString());
        logger.info("Plate {} is used by a car",car1.plate);

        // Press Ctrl+R or click the green arrow button in the gutter to run the code.
        for (int i = 1; i <= 2; i++) {

            x = i*i;
            // Press Ctrl+D to start debugging your code. We have set one breakpoint
            // for you, but you can always add more by pressing Cmd+F8.
            logger.info("i={}, x={}.",i, x);
        }

        var myCars = new ArrayList<Car>();
        for (int i=1; i <= 15; i++) {
            myCars.add(new Car("Seat"));
        }


        logger.info("1st {}",myCars.get(0).toString());

        for (Car car : myCars) {
            logger.info("Plate:{}, speed:{}",car.plate,car.speed);
        }


    }
}