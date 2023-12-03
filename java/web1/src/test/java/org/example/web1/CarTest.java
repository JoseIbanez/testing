package org.example.web1;

import org.example.web1.model.Car;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

//import org.assertj.core.api.Assertions;

public class CarTest {

    @Test
    public void testCarPlate() {
        var car = new Car("Tesla");
        Assertions.assertNotNull(car);
        Assertions.assertTrue(car.plate.matches(".*[A-Z]{3}$"),"Plate has to finish with 3 capital letters");
        Assertions.assertTrue(car.plate.matches("^[0-9]{4}.*"),"Plate has to start with 4 numbers");
    }

    @Test
    public void testCarMarker() {
        var marker1 = "Seat";
        var plate1 = "0001AAB";
        var marker2 = "Tesla";
        var plate2 = "3232FWD";

        var car1 = new Car(marker1, plate1);
        var car2 = new Car(marker2, plate2);

        Assertions.assertEquals(car1.getMaker(),marker1);
        Assertions.assertEquals(car1.plate, plate1);

        Assertions.assertEquals(car2.getMaker(),marker2);
        Assertions.assertEquals(car2.plate, plate2);

    }

    @Test
    public void testCarSpeed() {
        var car = new Car("Tesla");
        Assertions.assertNotNull(car);
        Assertions.assertEquals(car.speed,0);
    }

    @Test
    public void testSerialNumber() {
        var car = new Car("Tesla");

        Assertions.assertNotNull(car.getSerialNumber());

        var sn1 = "Test";
        car.setSerialNumber(sn1);
        Assertions.assertNotEquals(car.getSerialNumber(),sn1);

        var sn2 = "3a62b43e-39f8-4522-8d18-191afeac4f83";
        car.setSerialNumber(sn2);
        Assertions.assertEquals(car.getSerialNumber(),sn2);

    }



}
