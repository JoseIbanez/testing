#include <Arduino.h>
#include <gtest/gtest.h>
#include <calculator.h>
#include <unity.h>

Calculator calc;


namespace {
    class Calcula : public ::testing::Test {
        protected:
    };


    TEST_F(Calcula, Add1) {
        EXPECT_EQ(calc.add(25, 7), 32);
    }

    TEST_F(Calcula, Add2) {
        ASSERT_EQ(calc.add(25, 7), 32);
    }


    TEST_F(Calcula, Sub1) {
        EXPECT_EQ(calc.sub(25, 7), 32);
        ASSERT_EQ(calc.sub(25, 7), 32);
    }

    TEST_F(Calcula, Sub2) {
        ASSERT_EQ(calc.sub(25, 7), 18);
    }


}  // namespace





void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT);
    testing::InitGoogleTest();
}

void loop() {
    Serial.println("Hello world!");
    delay(1000);

    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);

    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);

    RUN_ALL_TESTS();
    delay(10000);
}
