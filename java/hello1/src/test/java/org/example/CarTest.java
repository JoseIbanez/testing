package org.example;

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


}
