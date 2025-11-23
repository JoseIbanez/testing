package main

import (
	"bufio"
	"compress/gzip"
	"log"
	"os"
)

type Writer struct {
	full_filename string
	fo            *os.File
	gf            *gzip.Writer
	fw            *bufio.Writer
}

func NewWriter(path string, filename string) (*Writer, error) {

	full_filename := path + filename + ".gz"

	// Create or open the file for writing
	fo, err := os.Create(full_filename)
	if err != nil {
		return nil, err
	}

	// Create a gzip writer
	gf := gzip.NewWriter(fo)
	fw := bufio.NewWriter(gf)

	// Create the Writer struct
	w := Writer{
		full_filename: full_filename,
		fo:            fo,
		gf:            gf,
		fw:            fw,
	}
	return &w, nil
}

// Defer closes all files
func (w *Writer) Defer() {

	w.fw.Flush()
	w.gf.Close()
	if err := w.fo.Close(); err != nil {
		log.Printf("Error closing file: %s", err)
	}
}

// Write data to the file
func (w *Writer) Write(data string) error {

	_, err := w.fw.Write([]byte(data))
	return err

}
