package main

import (
	"fmt"

	"net/http"
	"regexp"

	"path/filepath"

	"github.com/gocolly/colly/v2"
)

type Event struct {
	Date         string
	Championship string
	Local        string
	Visit        string
	Channels     string
}

func parse_table(e *colly.HTMLElement, eventList []Event) {

	date_list := []string{}
	date_re := regexp.MustCompile(`(\d+/\d+/\d+)`)

	e.ForEach("tbody > tr", func(_ int, tr *colly.HTMLElement) {

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
		event := Event{}
		if cols == 5 {
			event.Date = date + " " + tr.ChildText("td:nth-child(1)")
			event.Championship = tr.ChildText("td:nth-child(2)")
			event.Local = tr.ChildText("td:nth-child(3)")
			event.Visit = tr.ChildText("td:nth-child(4)")
			event.Championship = tr.ChildText("td:nth-child(5)")
		} else if cols == 4 {
			event.Date = date + " " + tr.ChildText("td:nth-child(1)")
			event.Championship = tr.ChildText("td:nth-child(2)")
			event.Local = tr.ChildText("td:nth-child(3)")
			event.Visit = tr.ChildText("td:nth-child(4)")
			event.Championship = tr.ChildText("td:nth-child(5)")
		} else {
			return
		}

		fmt.Printf("%v\n", event)
		eventList = append(eventList, event)

	})

}

func main() {
	// scraping logic...

	t := &http.Transport{}
	t.RegisterProtocol("file", http.NewFileTransport(http.Dir("/")))

	c := colly.NewCollector()
	c.WithTransport(t)

	eventList := make([]Event, 0)

	c.OnHTML("table.tablaPrincipal", func(e *colly.HTMLElement) {
		parse_table(e, eventList)
	})

	c.OnScraped(func(r *colly.Response) {
		fmt.Println(r.Request.URL, " scraped!")
	})

	fmt.Println("Hello, World!")

	absPath, _ := filepath.Abs("./sample-date/fetv.html")
	c.Visit("file://" + absPath)

	c.Wait()

}
