#include <calculator.h>
#include <stdio.h>
//#include <unity.h>

Calculator calc;

void test_function_calculator_addition(void) {
    int ret;
    ret = calc.add(25, 7);
    printf("%d",ret);
}

void test_function_calculator_subtraction(void) {
    calc.sub(23, 3);
}


int main(int argc, char **argv) {
    test_function_calculator_addition();
    return 0;
}

