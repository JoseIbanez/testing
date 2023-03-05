module example/p1

go 1.20

require (
	example/greetings v0.0.0-00010101000000-000000000000
	github.com/tidwall/gjson v1.14.4
	rsc.io/quote v1.5.2
)

replace example/greetings => ./greetings

require (
	github.com/tidwall/match v1.1.1 // indirect
	github.com/tidwall/pretty v1.2.0 // indirect
	golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c // indirect
	rsc.io/sampler v1.3.0 // indirect
)
