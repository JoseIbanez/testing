from kafka import KafkaConsumer
consumer = KafkaConsumer('quickstart-events')

consumer = KafkaConsumer(
    'quickstart-events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='smallest'
)

#print(consumer) 

for msg in consumer:
    print (msg)