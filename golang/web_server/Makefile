init:
	go mod init example/web_server
	go mod tidy

tidy:
	go mod tidy

build:
	go build

wasm:
	GOOS=js GOARCH=wasm go build -o main.wasm

run:
	go run .
