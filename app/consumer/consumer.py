import os
import json
from kafka import KafkaConsumer

kafka_broker = os.environ.get("KAFKA_BROKER_URL")
kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_broker.split(","),
    security_protocol="SSL",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print("Listening...")

for msg in consumer:
    print(f"Received message: {msg.value}")