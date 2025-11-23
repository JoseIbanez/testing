module example/kafka-producer

go 1.22.4

replace example/dto => ./dto

require (
	example/dto v0.0.0-00010101000000-000000000000
	github.com/confluentinc/confluent-kafka-go v1.9.2
	github.com/google/uuid v1.6.0
)
