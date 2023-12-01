package main

import (
	"bufio"
	"fmt"
	"os"
)


type Animal interface {
	Eat()
	Move()
	Speak()
}

type AnimalMap map[string]Animal

type Cow struct {}
type Bird struct {}
type Snake struct {}


func (a Cow) Eat() {
	fmt.Printf("is a %T and eats grass",a)
}

func (a Bird) Eat() {
	fmt.Printf("is a %T and eats worms",a)
}

func (a Snake) Eat() {
	fmt.Printf("is a %T and eats mice",a)
}

func (a Cow) Move() {
	fmt.Printf("is a %T and moves by walk",a)
}

func (a Bird) Move() {
	fmt.Printf("is a %T and moves by fly",a)
}

func (a Snake) Move() {
	fmt.Printf("is a %T and moves by slither",a)
}

func (a Cow) Speak() {
	fmt.Printf("is a %T and its sound is moo",a)
}

func (a Bird) Speak() {
	fmt.Printf("is a %T and its sound is peep",a)
}

func (a Snake) Speak() {
	fmt.Printf("is a %T and its sound is hsss",a)
}


func main() {

	animal_list := make(AnimalMap)

	//fmt.Printf("%v\n",animal_list)

	for {

		cmd, arg1, arg2, err := get_input_request()
		//fmt.Printf("cmd: %s %s\n",animal_req,info_req)
		if err != nil {
			continue
		}

		if cmd == "newanimal" {
			add_new_animall(animal_list, arg1, arg2)
			continue
		} else if  cmd == "query" {
			query_animal(animal_list, arg1, arg2)
			continue
		} else {
			fmt.Printf("Unknown cmd:%s",cmd)
			continue
		}



	}
}

func add_new_animall(animal_list AnimalMap, name string, animal_type string) {

	var animal_interface Animal
	
	if animal_type == "cow" {
		animal_interface = Cow{}
	} else if animal_type == "bird" {
		animal_interface = Bird{}
	} else if animal_type == "snake" {
		animal_interface = Snake{}
	} else {
		fmt.Printf("I don't knwo this animal type %s",animal_type)
		return
	}

	animal_list[name] = animal_interface

	fmt.Printf("%s, Created it!\n",name)


}


func query_animal(animal_list AnimalMap, name string, action string) {

	animal, ok := animal_list[name]
	if ! ok {
		fmt.Printf("animal %s, not found in my DB\n",name)
		return
	}

	if action == "eat" {
		animal.Eat()
	} else if action == "move" {
		animal.Move()
	} else if action == "speak" {
		animal.Speak()
	} else {
		fmt.Printf(" we don't know about %s",action)
	}
	fmt.Println()

}



func get_input_request() (string, string, string, error) {

	fmt.Print("> ")
	var input_string string

	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		input_string = scanner.Text()
	}

	if len(input_string) <= 0 {
		return "", "", "", fmt.Errorf("no input")
	}

	var cmd string
	var arg1 string
	var arg2 string
	var n int
	var err error

	n, err = fmt.Sscanf(input_string, "%s %s %s", &cmd, &arg1, &arg2)
	if n<2 || err != nil {
		return "", "", "", err
	}

	return cmd, arg1, arg2, nil

}