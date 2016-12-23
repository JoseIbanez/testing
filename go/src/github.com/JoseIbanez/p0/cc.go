package main 

import (
	"fmt"
	"time" ) 


func say(s string) {
	for i := 0; i < 500; i++ {
		time.Sleep(100 * time.Millisecond)
		fmt.Println(s)
	}
}

func main() {
	go say("world")
	go say("hello")
	go say("go")

	time.Sleep(50 * time.Second)
}
