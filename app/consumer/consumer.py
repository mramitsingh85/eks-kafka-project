from kafka import KafkaConsumer
import ssl
import json
import os

kafka_broker = os.environ.get("KAFKA_BROKER_URL")
kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

context = ssl.create_default_context()

consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_broker.split(","),
    security_protocol="SSL",
    ssl_context=context,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening...")

for msg in consumer:
    print(msg.value)