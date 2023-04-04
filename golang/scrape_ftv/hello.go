package main

import (
	"fmt"

	"net/http"
	"regexp"

	"github.com/gocolly/colly/v2"
)

type Event struct {
	Date          string
	Championship  string 
	Local         string
	Visit         string
	Channels      string
}


func main() {
	// scraping logic...

	t := &http.Transport{}
	t.RegisterProtocol("file", http.NewFileTransport(http.Dir("/")))

	c := colly.NewCollector()
	c.WithTransport(t)

	eventList = make []EveEvent

	c.OnHTML("table.tablaPrincipal", func(e *colly.HTMLElement) {
		//fmt.Println("tablaPrincipal")
		//fmt.Println(e.Text)

		date_list := []string{}
		//even_list := []string{}

		date_re := regexp.MustCompile(`(\d+/\d+/\d+)`)

		e.ForEach("tbody > tr", func(_ int, tr *colly.HTMLElement) {
			//fmt.Println(tr.Text)

			if tr.Index == 0 {
				date := tr.ChildText("td:nth-child(1)")
				match := date_re.FindStringSubmatch(date)
				if len(match) > 0 {
					date_list = append(date_list, match[1])
				}
				return
			}

			if len(date_list) < 1 {
				return
			}

			cols := len(tr.DOM.Children().Nodes)
			date := date_list[0]

			if cols == 5 {
				hour := date + " " + tr.ChildText("td:nth-child(1)")
				championship := tr.ChildText("td:nth-child(2)")
				//local        := tr.ChildText("td:nth-child(3)")
				//visit        := tr.ChildText("td:nth-child(4)")
				//channels     := tr.ChildText("td:nth-child(5)")

				fmt.Println(hour + " " + championship)

			} else if cols == 4 {
				hour := date + " " + tr.ChildText("td:nth-child(1)")
				championship := tr.ChildText("td:nth-child(2)")
				//local        := tr.ChildText("td:nth-child(3)")
				//visit        := ""
				//channels     := tr.ChildText("td:nth-child(4)")

				fmt.Println(hour + " " + championship)

			}

		})

	})

	c.OnScraped(func(r *colly.Response) {
		fmt.Println(r.Request.URL, " scraped!")
	})

	fmt.Println("Hello, World!")

	c.Visit("file:///Users/ibanez/Projects/testing/golang/scrape_ftv/sample-date/fetv.html")
	c.Wait()

}
