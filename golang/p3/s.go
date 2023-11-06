package main

import "fmt"

type P struct {
	x string
	y int
}

func main() {
	b := P{"x", -1}
	a := [...]P{P{"a", 10},
		P{"b", 2},
		P{"c", 3}}
	for _, z := range a {
		if z.y > b.y {
			b = z
		}
	}
	fmt.Println(b.x)
}
