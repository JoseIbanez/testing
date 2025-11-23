package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)


type User struct {
	fname string
	lname string
}


func main() {
 
	user_list := []User {}
	filename := "sample.txt"
	var err error

	fmt.Print("Enter a filename: ")

	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		filename = scanner.Text()
	}



	user_list, err = load_file(filename, user_list)
	if err != nil {
		return
	}

	fmt.Printf("%v",user_list)

}



func load_file(filename string, user_list []User) ([]User, error) {

	file, err := os.Open(filename)
    if err != nil {
        log.Fatal(err)
		return []User {}, err
	}
    defer file.Close()


    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
		var fname string
		var lname string
		var n int
		var err error


		line := scanner.Text()
		//fmt.Println(line)

		n,err = fmt.Sscanf(line,"%s %s",&fname,&lname)
		if n < 1 || err != nil {
			continue
		} 

		//fmt.Printf("fname:%s lname:%s\n",fname,lname)
		user_list = append(user_list, User{fname: fname, lname: lname })

	}

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
		return []User {}, err
	}

    return user_list, err
}