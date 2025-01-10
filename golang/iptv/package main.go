package main

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestParseW3UFile_ValidFile(t *testing.T) {
	// Create a mock .w3u file
	mockFileContent := `{
		"name": "Test List",
		"author": "Test Author",
		"groups": [
			{"name": "Test Link 1", "url": "http://example.com/stream1.m3u", "image": "http://example.com/image1.jpg", "info": "Info 1"},
			{"name": "Test Link 2", "url": "http://example.com/stream2.m3u8", "image": "http://example.com/image2.jpg", "info": "Info 2"}
		]
	}`
	mockFileName := "test_valid.w3u"
	ioutil.WriteFile(filepath.Join("cache", mockFileName), []byte(mockFileContent), 0644)
	defer os.Remove(filepath.Join("cache", mockFileName))

	// Call the function
	result := parseW3UFile(mockFileName)

	// Assertions
	assert.Equal(t, 2, len(result))
	assert.Equal(t, "Test Link 1", result[0].Name)
	assert.Equal(t, "http://example.com/stream1.m3u", result[0].Url)
	assert.Equal(t, "http://example.com/image1.jpg", result[0].Image)
	assert.Equal(t, "Info 1", result[0].Info)
	assert.Equal(t, "stream1.m3u", result[0].Filename)
}

func TestParseW3UFile_InvalidJSON(t *testing.T) {
	// Create a mock .w3u file with invalid JSON
	mockFileContent := `{
		"name": "Test List",
		"author": "Test Author",
		"groups": [
			{"name": "Test Link 1", "url": "http://example.com/stream1.m3u", "image": "http://example.com/image1.jpg", "info": "Info 1"
	}`
	mockFileName := "test_invalid_json.w3u"
	ioutil.WriteFile(filepath.Join("cache", mockFileName), []byte(mockFileContent), 0644)
	defer os.Remove(filepath.Join("cache", mockFileName))

	// Call the function
	result := parseW3UFile(mockFileName)

	// Assertions
	assert.Equal(t, 0, len(result))
}

func TestParseW3UFile_UnsupportedExtension(t *testing.T) {
	// Create a mock .w3u file with unsupported extension
	mockFileContent := `{
		"name": "Test List",
		"author": "Test Author",
		"groups": [
			{"name": "Test Link 1", "url": "http://example.com/stream1.mp4", "image": "http://example.com/image1.jpg", "info": "Info 1"}
		]
	}`
	mockFileName := "test_unsupported_extension.w3u"
	ioutil.WriteFile(filepath.Join("cache", mockFileName), []byte(mockFileContent), 0644)
	defer os.Remove(filepath.Join("cache", mockFileName))

	// Call the function
	result := parseW3UFile(mockFileName)

	// Assertions
	assert.Equal(t, 0, len(result))
}

func TestParseW3UFile_PhpExtension(t *testing.T) {
	// Create a mock .w3u file with .php extension
	mockFileContent := `{
		"name": "Test List",
		"author": "Test Author",
		"groups": [
			{"name": "Test Link 1", "url": "http://example.com/stream1.php", "image": "http://example.com/image1.jpg", "info": "Info 1"}
		]
	}`
	mockFileName := "test_php_extension.w3u"
	ioutil.WriteFile(filepath.Join("cache", mockFileName), []byte(mockFileContent), 0644)
	defer os.Remove(filepath.Join("cache", mockFileName))

	// Call the function
	result := parseW3UFile(mockFileName)

	// Assertions
	assert.Equal(t, 1, len(result))
	assert.Equal(t, "Test Link 1", result[0].Name)
	assert.Equal(t, "http://example.com/stream1.php", result[0].Url)
	assert.Equal(t, "http://example.com/image1.jpg", result[0].Image)
	assert.Equal(t, "Info 1", result[0].Info)
	assert.Equal(t, "Test_Link_1.m3u", result[0].Filename)
}