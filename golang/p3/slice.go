package main

import (
	"fmt"
	"sort"
)

func main() {

	var integer_list []int
	var input int

	for {

		_, err := fmt.Scanf("%d", &input)

		if err != nil {
			fmt.Println("Done.")
			return
		}

		integer_list = append(integer_list, input)
		sort.Ints(integer_list)

		fmt.Printf("List: %v\n", integer_list)

	}

}
