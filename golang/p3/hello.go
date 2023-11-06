package main

import (
	"fmt"
	"strings"
)

func main() {

	println("Hello, world!")

	s := strings.Replace("ianianian", "ni", "in", 2)
	fmt.Println(s)

	var xtemp int
	x1 := 0
	x2 := 1
	for x := 0; x < 5; x++ {
		xtemp = x2
		x2 = x2 + x1
		x1 = xtemp
	}
	fmt.Println(x2)

	x := map[string]int{
		"ian": 1, "harris": 2}
	for i, j := range x {
		if i == "harris" {
			fmt.Print(i, j)
		}
	}

	xx := []int{1, 2, 3, 4, 5}
	y := xx[0:2]
	z := xx[1:4]
	fmt.Print(len(y), cap(y), len(z), cap(z))

}
