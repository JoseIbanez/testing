package main

import (
	"log"
	"net/url"
	"strings"
)

type SimpleParam struct {
	param string
	value string
}

type RangeParam struct {
	param string
	lower_operator string
	lower_value string
	upper_operator string
	upper_value string
}


func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	//simpleList := make(map[string]SimpleParam)
	rangeList := []RangeParam{}

	u, err := url.Parse("https://example.org/topic/334/event?eventType=log&event.metric.name=metric&eventTime.gt=2024-01-01T09:00:00&eventTime.lt=2024-01-01T09:00:00&source.name=resourceA%3BresourceB&source.label.label1=value")
	log.Println(u)
	if err != nil {
		log.Fatal(err)
	}

	q := u.Query()
	log.Println(q)


	for param, value := range q {

		paramItems := strings.Split(param, ".")
		lastItem := paramItems[len(paramItems)-1] 
		log.Println(lastItem)

		log.Println(param,value)
		if lastItem == "lt" || lastItem == "lte" {
			queryItem := RangeParam{param,lastItem,value[0],"",""}
			rangeList=append(rangeList,queryItem)
			log.Println(lastItem)
			log.Println(queryItem)
		}

    log.Println(rangeList)


	}



}
