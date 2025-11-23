module example/p1

go 1.20

require (
	example/greetings v0.0.0-00010101000000-000000000000
<<<<<<< HEAD
	github.com/tidwall/gjson v1.14.4
=======
	example/myuser v0.0.0-00010101000000-000000000000
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
	rsc.io/quote v1.5.2
)

replace example/greetings => ./greetings

<<<<<<< HEAD
require (
	github.com/tidwall/match v1.1.1 // indirect
	github.com/tidwall/pretty v1.2.0 // indirect
	golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c // indirect
	rsc.io/sampler v1.3.0 // indirect
=======
replace example/myuser => ./myuser

require (
	github.com/tidwall/gjson v1.17.0 // indirect
	github.com/tidwall/match v1.1.1 // indirect
	github.com/tidwall/pretty v1.2.0 // indirect
	golang.org/x/text v0.13.0 // indirect
	rsc.io/sampler v1.99.99 // indirect
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
)
