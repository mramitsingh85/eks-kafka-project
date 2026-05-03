import os
from kafka import KafkaConsumer
import json
import time

kafka_broker = os.environ.get("KAFKA_BROKER_URL")
kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=[kafka_broker],
    group_id="my-consumer-group-v3",  # 
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print(f"Listening for messages on topic '{kafka_topic}'...")

for message in consumer:
    print(f"Received message: {message.value}")
    time.sleep(2)  # 🔥 simulate slow processing (creates lag)