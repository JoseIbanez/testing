package main

import (
	"encoding/json"
	"fmt"
	"bufio"
	"os"
)

func main() {

	var name string
	var address string
	var scanner *bufio.Scanner

	fmt.Print("Enter your name: ")
	scanner = bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		name = scanner.Text()
	}

	fmt.Print("Enter your address: ")
	scanner = bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		address = scanner.Text()
	}



	user := map[string]string {
		"name": name,
		"address": address,
	}


	output, err := json.Marshal(user)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Printf(string(output))

}