package greetings

import (
<<<<<<< HEAD
	"errors"
	"fmt"
	"log"
=======
    "errors"
    "fmt"
    "log"
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
)

// Hello returns a greeting for the named person.
func Hello(name string) (string, error) {
<<<<<<< HEAD
	// If no name was given, return an error with a message.
	if name == "" {

		log.SetPrefix("greetings: ")
		log.SetFlags(0)

		err := errors.New("empty name")
		log.Println(err)
		return "", err
	}

	// If a name was received, return a value that embeds the name
	// in a greeting message.
	message := fmt.Sprintf("Hi, %v. Welcome!", name)
	return message, nil
=======
    // If no name was given, return an error with a message.
    if name == "" {

        log.SetPrefix("greetings: ")
        log.SetFlags(0)

        err := errors.New("empty name")
        log.Println(err)
        return "", err
    }

    // If a name was received, return a value that embeds the name
    // in a greeting message.
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    return message, nil
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
}
