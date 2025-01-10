package main

import (
	"fmt"
	"log"
)


func consumer(queue chan Link, done chan bool, name string) {
	for {
		link, more := <-queue
		log.Printf("Consumer %s got link %v", name, link.Filename)
		if !more {
			done <- true
			return
		}
		DownloadFile(link.Filename, link.Url)
	}
}


func parse_w3u_files_async() {

	queue := make(chan Link, 100)
	done := make(chan bool)

	for i := 0; i < 5; i++ {
		go consumer(queue,done,fmt.Sprintf("consumer%v",i))
	}

	w3u_files := get_w3u_files()
	for _, file := range w3u_files {
		link_list := parseW3UFile(file)

		for _, link := range link_list {
			//	DownloadFile(link.Filename, link.Url)
			queue <- link
		}	

	}
	close(queue)

	<- done


}


