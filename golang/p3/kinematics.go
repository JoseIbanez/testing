package main

import (
	"fmt"
	"math"
)


func main () {

	var a, v0, s0, s1, t float64

	fmt.Println("Enter these parameters...")
	fmt.Print("acceleration, a:")
	fmt.Scanf("%f",&a)
	fmt.Print("initial speed, v0:")
	fmt.Scanf("%f",&v0)
	fmt.Print("initial displacement, s0:")
	fmt.Scanf("%f",&s0)


	fmt.Printf("Time=0, a=%f v0=%f s0=%f\n",a,v0,s0)
	fn_displace := GenDisplaceFn(a, v0, s0)

	for {

		fmt.Print("now, a time delay, t:")
		fmt.Scanf("%f",&t)

		s1 = fn_displace(t)

		fmt.Printf("Current position:\nTime=%f s1:%f\n",t,s1)

	}

}



func GenDisplaceFn(a , v0, s0 float64) func (float64) float64 {


	fn_displace := func(t float64) float64 {
		s := 0.5 * a *  math.Pow(t, 2) + v0 * t + s0
		return s
	}
	return fn_displace


}

