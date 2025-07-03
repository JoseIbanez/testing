build:
	go build -ldflags \
		"-X main.buildVersion=${shell git describe --tags}"

init:
	go mod init esm/elastic
	go mod tidy

tidy:
	go mod tidy

run:
	go run .

clean:
	rm p1
