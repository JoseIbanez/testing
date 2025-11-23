package main

import (
	"fmt"
)

func main() {

	var number float32
	var result int

	fmt.Print("Enter a float number, please: ")
	fmt.Scanf("%f", &number)

	result = int(number)
	fmt.Printf("The ingenter part of %f is %d", number, result)

}
