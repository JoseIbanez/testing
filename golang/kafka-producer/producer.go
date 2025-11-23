package main

import (
	"encoding/json"
	"example/dto"
	"log"
	"time"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/google/uuid"
)

const (
	KafkaServer = "localhost:29092"
	KafkaTopic  = "orders-v1-topic"
)

func main() {

	log.SetPrefix("greetings: ")
	log.SetFlags(0)

	log.Printf("Connecting to kafka:%s\n", KafkaServer)

	p, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": KafkaServer,
	})
	if err != nil {
		panic(err)
	}
	defer p.Close()

	topic := KafkaTopic
	order := dto.Order{
		ID:        uuid.New().String(),
		ProductId: uuid.New().String(),
		UserId:    uuid.New().String(),
		Amount:    456000,
	}

	value, err := json.Marshal(order)
	if err != nil {
		panic(err)
	}

	log.Printf("Sending to kafka, id:%s\n", order.ID)

	err = p.Produce(&kafka.Message{
		TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
		Value:          value,
	}, nil)

	if err != nil {
		panic(err)
	}

	log.Printf("Done.")

	time.Sleep(1 * time.Second)

}
