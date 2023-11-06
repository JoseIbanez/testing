package main

import (
	"bufio"
	"fmt"
	"os"
)


type Animal struct {
	food string
	locomotion string
	noise string
}


func (animal *Animal) Eat() {
	fmt.Print(animal.food)
}

func (animal *Animal) Move() {
	fmt.Print(animal.locomotion)
}

func (animal *Animal) Speak() {
	fmt.Print(animal.noise)
}

func main() {

	animal_list := make(map[string]Animal)
	load_animals(animal_list)

	//fmt.Printf("%v\n",animal_list)

	for {

		animal_req, info_req, err := get_input_request()
		//fmt.Printf("cmd: %s %s\n",animal_req,info_req)
		if err != nil {
			continue
		}


		animal_selected, ok := animal_list[animal_req]
		if ! ok {
			fmt.Printf("animal %s, not found in my DB",animal_req)
			continue
		}


		if info_req == "eat" {
			fmt.Printf("%s eats ... ",animal_req)
			animal_selected.Eat()
		} else if info_req == "move" {
			fmt.Printf("%s, its method of locomotion is ... ",animal_req)
			animal_selected.Move()
		} else if info_req == "speak" {
			fmt.Printf("%s, the sound it makes when it speaks is ... ",animal_req)
			animal_selected.Speak()
		} else {
			fmt.Printf("I don't know wath a %s makes for %s",animal_req,info_req)
		}
		fmt.Println(".")


	}
}


func load_animals(animal_list map[string]Animal) error {

	animal_list["cow"] = Animal{food: "grass", locomotion: "walk", noise: "moo" }
	animal_list["bird"] = Animal{food: "worms", locomotion: "fly", noise: "peep" }
	animal_list["snake"] = Animal{food: "mice", locomotion: "slither", noise: "hsss" }
	return nil

}


func get_input_request() (string, string, error) {

	fmt.Print("> ")
	var input_string string

	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		input_string = scanner.Text()
	}

	if len(input_string) <= 0 {
		return "", "", fmt.Errorf("no input")
	}

	var animal_req string
	var info_req string
	var n int
	var err error

	n, err = fmt.Sscanf(input_string, "%s %s", &animal_req,&info_req)
	if n<2 || err != nil {
		return "", "", err
	}

	return animal_req, info_req, nil

}