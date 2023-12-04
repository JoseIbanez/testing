package org.example.web1;

import org.example.web1.dao.FakeDB;
import org.example.web1.model.Car;
import org.junit.jupiter.api.Test;


public class FakeDBTest {


    @Test
    public void testDBload() {

        var DB = new FakeDB();

        var car1 = new Car("Seat", "3434DDF");
        var car2 = new Car("BMW", "0001CFG");

        DB.updateCar(car1);
        DB.updateCar(car2);

        DB.saveToFile();
        DB.loadFromFile();

    }


    @Test
    public void testBufferCounter() {

        FakeDB DB = new FakeDB();

        for (int i=0; i <20; i++) {

            var car = new Car("Seat");
            DB.updateCar(car);

        }

    }



}
