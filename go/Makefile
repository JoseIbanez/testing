# This is how we want to name the binary output
BINARY=test

# These are the values we want to pass for Version and BuildTime
VERSION=0.0.1
BUILD_TIME=`date +%FT%T%z`

# Setup the -ldflags option for go build here, interpolate the variable values
#LDFLAGS=-ldflags "-X github.com/ariejan/roll/core.Version=${VERSION} -X github.com/ariejan/roll/core.BuildTime=${BUILD_TIME}"
LDFLAGS=

all:
	#go build ${LDFLAGS} -o ${BINARY} test1.go
	go build github.com/JoseIbanez/cdr
	go install github.com/JoseIbanez/hello
	echo "a,b,c" | hello
