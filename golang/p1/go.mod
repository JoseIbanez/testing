module example/p1

go 1.20

require (
	example/greetings v0.0.0-00010101000000-000000000000
	github.com/tidwall/gjson v1.17.0
	rsc.io/quote v1.5.2
)

replace example/greetings => ./greetings

require (
	github.com/tidwall/match v1.1.1 // indirect
	github.com/tidwall/pretty v1.2.1 // indirect
	golang.org/x/text v0.13.0 // indirect
	rsc.io/sampler v1.99.99 // indirect
)
