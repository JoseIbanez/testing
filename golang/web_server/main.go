package main

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

type Book struct {
	ID     uint   `json:"id" gorm:"primary_key"`
	Title  string `json:"title"`
	Author string `json:"author"`
	Price  uint
}

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "hello world"})
	})

	r.GET("/test", func(c *gin.Context) {

		b1 := Book{
			ID:     32323,
			Title:  "My Book",
			Author: "yo",
			Price:  300,
		}

		log.SetFlags(log.LstdFlags | log.Lshortfile)
		log.Println("b1",b1,"b2","2")
		b1.ID = b1.ID + 1

		//result := gin.H{"data": "test", "result": 0, "b": gin.H{"c": 3}}
		c.JSON(http.StatusOK, b1)

	})

	r.Run()
}
