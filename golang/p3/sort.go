package main

import (
	"fmt"
	"slices"
)

func my_sort(chunk []int, channel chan []int) {
	/* sort small array */

	original := make([]int, len(chunk))
	copy(original, chunk)
	slices.Sort(chunk)

	fmt.Printf("Chunk sort: %v -> %v\n", original, chunk)
	channel <- chunk
}

func send_tasks(list []int, channel chan []int) {
	/*  split array,
	send small chuck to gorutine
	*/

	chunk_size := len(list) / 4

	for i := 0; i < 4; i++ {

		from := i * chunk_size
		to := (i + 1) * chunk_size

		if i == 3 {
			to = len(list)
		}

		chunk := list[from:to]

		go my_sort(chunk, channel)

	}

}

func receive_results(channel chan []int) []int {

	medium_list := []int{}

	for i := 0; i < 4; i++ {
		chunk := <-channel
		medium_list = append(medium_list, chunk...)
		//fmt.Println(medium_list)
	}

	fmt.Printf("Partial sorted list: %v\n", medium_list)

	return medium_list

}

func get_input_list() []int {

	list := []int{}

	fmt.Println("Enter a sequence of integers to sort, one per line, empty line to end")
	for index := 0; true; index++ {
		var value int

		count, err := fmt.Scanf("%d\n", &value)

		if count < 1 || err != nil {
			break
		}

		list = append(list, value)

	}
	return list

}

func main() {

	//list := []int{3, 4, 5, 6, 6, 3, 34, 44, 34, 6, 4, 33, 49, 2}

	list := get_input_list()

	channel := make(chan []int, 10)

	send_tasks(list, channel)
	final_list := receive_results(channel)

	/* Final sort */
	slices.Sort(final_list)
	fmt.Printf("Final result: %v\n", final_list)

}
