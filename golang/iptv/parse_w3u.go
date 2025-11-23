package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/url"
	"os"
	"path/filepath"
	"slices"
	"strings"

	"github.com/tidwall/gjson"
)


type Link struct {
	Name    string  `json:"name"`
	Filename string `json:"filename"`
	Url 	string  `json:"url"`
	Image   string  `json:"image"`
	Info    string `json:"info"`
}


func parseW3UFile(name string) ([]Link) {

	// Open the file
	filePath := fmt.Sprintf("cache/%s", name)
	file, err := os.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	// Close the file
	defer file.Close()

	// Read the file
	byteValue, _ := io.ReadAll(file)


	var result []Link

	list_name := gjson.GetBytes(byteValue, "name").Str
	list_author := gjson.GetBytes(byteValue, "author").Str
	log.Printf("Name: %s Author: %s", list_name, list_author)

	value := gjson.GetBytes(byteValue, "groups")
	if value.Index <= 0 {
		log.Printf("No groups found in file %s", filePath)
		os.WriteFile(filePath+".done", []byte("done"), 0755)
		return []Link{}
	}
	raw := byteValue[value.Index : value.Index+len(value.Raw)]

	//parse json array
	var link_list []Link
	err = json.Unmarshal(raw, &link_list)
	if err != nil {
		log.Printf("Error parsing file: %s, err:%s ",filePath, err)
		os.WriteFile(filePath+".done", []byte("done"), 0755)
		return []Link{}
	}

	for _, link := range link_list {

		filename_url, err := FilenameFromUrl(link.Url)
		if err != nil {
			continue
		}
		link.Filename = filename_url

		//check file extension
		ext := filepath.Ext(filename_url)
		if ext == ".php" {
			link.Filename = strings.Replace(link.Name + ".m3u", " ", "_", -1)
		} else if ext != ".m3u" && ext != ".m3u8" && ext != ".w3u" {
			log.Printf("Invalid file %s, extension: %s", link.Url, ext)
			continue
		}

		log.Printf("Name:%s Url:%s Image:%s, Info: %s\n", link.Name, link.Url, link.Image, link.Info)
		result = append(result, Link{Name: link.Name, Url: link.Url, Image: link.Image, Info: link.Info, Filename: link.Filename})
	
	}


	log.Printf("Parsed %d links", len(result))
	os.WriteFile(filePath+".done", []byte("done"), 0755)

	return result
}



//FilenameFromUrl takes input as a escaped url & outputs filename from it (unescaped - normal one)
func FilenameFromUrl(urlstr string) (string, error) {
	u, err := url.Parse(urlstr)
	if err != nil {
		log.Println("Error due to parsing url: ", err)
		return "", err
	}
	x, _ := url.QueryUnescape(u.EscapedPath())
	return filepath.Base(x), nil
}


func get_w3u_files() ([]string) {

	files, err := os.ReadDir("cache/")
	if err != nil {
		log.Fatal(err)
	}

	// Get a list of file names (.w3u or .done)
	var file_names []string 
	for _, file := range files {
		file_name := file.Name()
		file_ext := filepath.Ext(file_name)
		if file_ext == ".w3u" || file_ext == ".done" {
			file_names = append(file_names, file_name)
		}
	}

	var result []string
	for _, file := range file_names {

		//check if the file is already processed
		if slices.Contains(file_names, file+".done") {
			log.Printf("File %s already processed", file)
			continue	
		}

		if filepath.Ext(file) == ".w3u" {
			result = append(result, file)
		}
	}
	return result
}

func parse_w3u_files() {

	w3u_files := get_w3u_files()
	for _, file := range w3u_files {
		link_list := parseW3UFile(file)

		for _, link := range link_list {
			DownloadFile(link.Filename, link.Url)
		}	

	}
}