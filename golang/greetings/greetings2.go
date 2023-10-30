package greetings

import (
	"errors"
	"fmt"
)

// Hello returns a greeting for the named person.
func Hello2(name string) (string, error) {

	if name == "" {
		return "", errors.New("empty name")
	}

	// Return a greeting that embeds the name in a message.
	message := fmt.Sprintf("Hi2, %v. Welcome!", name)
	return message, nil
}
