package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

// DownloadFile will download a url and store it in local filepath.
// It writes to the destination file as it downloads it, without
// loading the entire file into memory.
func DownloadFile(name string, url string) error {

	filePath := fmt.Sprintf("cache/%s", name)

	time0 := time.Now()

	// Check if the file already exists
	if _, err := os.Stat(filePath); err == nil {
		return fmt.Errorf("File %s already exists", filePath)
	}

	// Create the file
	out, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer out.Close()

	// Get the data
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Write the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return err
	}

	log.Printf("Downloaded %s in %s", name, time.Since(time0))

	return nil
}

func main() {

	log.SetPrefix("main: ")
	log.SetFlags(0)

	sample_url := "https://iptv-org.github.io/iptv/index.m3u"
	err := DownloadFile("index.m3u", sample_url)
	fmt.Println(err)

	sample_url = "https://af1c1onados.vercel.app/af1cionados.w3u"
	err = DownloadFile("af1cionados.w3u", sample_url)

	//sample_url = "https://af1c1onados.vercel.app/02.Menu.Iptvs.w3u"
	//err = DownloadFile("02.Menu.Iptvs.w3u", sample_url)
	fmt.Println(err)

	parse_w3u_files_async()

}
