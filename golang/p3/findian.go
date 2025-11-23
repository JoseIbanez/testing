package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {

	const NOT_FOUND = "Not found!"
	const FOUND = "Found!"
	var input_string = ""

	fmt.Print("Enter a string, please: ")

	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		input_string = scanner.Text()
	}

	if len(input_string) <= 0 {
		fmt.Println(NOT_FOUND)
		return
	}

	if input_string[0] != 'i' && input_string[0] != 'I' {
		fmt.Println(NOT_FOUND)
		return
	}

	if input_string[len(input_string)-1] != 'n' && input_string[len(input_string)-1] != 'N' {
		fmt.Println(NOT_FOUND)
		return
	}

	if strings.Index(input_string, "a") < 0 && strings.Index(input_string, "A") < 0 {
		fmt.Println(NOT_FOUND)
		return
	}

	fmt.Println(FOUND)

}
