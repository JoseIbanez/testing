package cdr

import (
	"log"
)

type Cdr struct {
	r []string
}

func (c *Cdr) PrepareCdr() int {
	log.Println("c",c)
  c.r = make([]string,4)
	log.Println("c",c)
	return 0
}

func (c *Cdr) UpdateCdr(f []string) int {
  log.Println("c",c)
	log.Println("f",f)
  c.r[0]=f[1]
	c.r[1]=f[2]
	log.Println(c.r)
	return 0
}
