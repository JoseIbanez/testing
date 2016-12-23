package main

import (
	"encoding/csv"
	"log"
	"os"
	"io"
)

func main() {
	/*
	records := [][]string{
		{"first_name", "last_name", "username"},
		{"Rob", "Pike", "rob"},
		{"Ken", "Thompson", "ken"},
		{"Robert", "Griesemer", "gri"},
	}
  */
	f1 := []string  { "", "" }

	r := csv.NewReader(os.Stdin)
	w := csv.NewWriter(os.Stdout)

  for {
		f, err := r.Read()
		if err == io.EOF {
			break
		} else if  err != nil {
			log.Fatalln("error reading csv:", err)
		}

    f1[0]=f[1]
		f1[1]=f[2]

	  log.Println(f)
    log.Println(f1)

	  w.Write(f1)
	  err = w.Error()
		if err != nil {
			log.Fatalln("error writing csv:", err)
		}

	}
	w.Flush()

}
