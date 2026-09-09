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

manual-test:
	go test -v ./...

clean:
	rm p1