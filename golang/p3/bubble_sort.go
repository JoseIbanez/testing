package main

import (
	"fmt"
	"log"
)


func main() {

	
	sli := make([]int,10)

	GetInputList(sli)
	fmt.Printf("Original:%v\n",sli)

	BubbleSort(sli)
	fmt.Printf("Result:%v\n",sli)

}

func GetInputList(sli []int) {

	fmt.Println("Enter a sequence of up to 10 integers to sort:")
	for index := 0; index <10; index++ {
		var value int

		count, err := fmt.Scanf("%d",&value)

		if count < 1 || err != nil {
			return
		}

		sli[index] = value

	}

}



func BubbleSort(sli []int) {


	for {
		next_round := false

		for index := 0 ; index < len(sli)-1 ; index ++ {

			if sli[index] > sli[index+1] {
				Swap(sli,index)
				next_round = true
			}

		}	
		fmt.Println("Bublle pass")

		if ! next_round {
			break
		}


	}

	fmt.Printf("Bubble sort done.\n")
}	


func Swap(sli []int, index int) {

	if index+1 > len(sli) {
		log.Printf("index is out of size, index:%d, slice size:%d",index,cap(sli))
		return
	}

	aux := sli[index]

	sli[index] = sli[index+1]
	sli[index+1] = aux
 

}