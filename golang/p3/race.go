package main

/*
Comments:

Race condition: when multiple actitivies are executed in parallel or seduo-parallel (concurrently)
and they access to a common resource, there is not guarantee in which order are executed.
We cannot predict the final result

Basic example: Three concurent tasks set the value of a global variable
*/

import (
	"fmt"
	"time"
)

var value int = 0

func set(val int) {
	for i := 0; i < 10; i++ {
		value = val
		time.Sleep(1 * time.Microsecond)
	}
}

func main() {

	go set(1)
	go set(2)
	go set(3)

	time.Sleep(1 * time.Millisecond)

	fmt.Print(value)

}
