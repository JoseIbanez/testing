package main

import (
	"fmt"
	"sync"
	"time"
)

type Chopstick struct {
	sync.Mutex
}

type Philo struct {
	id        int
	left_cho  *Chopstick
	right_cho *Chopstick
}

var host_token chan string
var wg sync.WaitGroup

func host() {

	host_token <- "1st"
	host_token <- "2nd"

	wg.Done()

}

func (p Philo) eat() {

	var token string

	for eat_counter := 1; eat_counter < 4; {

		/* ask host for permission */
		select {
		case token = <-host_token:
			{
				//fmt.Printf("I have host permission, philo:%d token:%s\n", p.id, token)
			}
		default:
			{
				//fmt.Printf("waiting for host permission, philo:%d\n", p.id)
				time.Sleep(1 * time.Second)
				continue
			}
		}

		/* get chopsticks */
		p.left_cho.Lock()
		p.right_cho.Lock()

		/* eat */
		fmt.Printf("starting to eat %d, time:%d\n", p.id, eat_counter)
		eat_counter++
		time.Sleep(1 * time.Second)
		fmt.Printf("finishing eating %d, time:%d\n", p.id, eat_counter)

		/* release chopstics */
		p.right_cho.Unlock()
		p.left_cho.Unlock()

		/* say host I'm done*/
		host_token <- token

	}
	wg.Done()

}

func main() {

	host_token = make(chan string, 2)

	philos := make([]*Philo, 5)
	chopsticks := make([]*Chopstick, 5)

	/* Prepare chopstic list */
	for i := 0; i < 5; i++ {
		chopsticks[i] = new(Chopstick)
	}

	/* Prepare philos list */
	for i := 0; i < 5; i++ {
		philos[i] = &Philo{i + 1, chopsticks[i], chopsticks[(i+1)%5]}
	}

	/* create the host tokens (permisions) */
	wg.Add(1)
	go host()

	/* start the dinner */
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go philos[i].eat()
	}

	wg.Wait()

}
