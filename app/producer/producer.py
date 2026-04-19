from kafka import KafkaProducer
import ssl
import json
import os
from datetime import datetime
import time

kafka_broker = os.environ.get("KAFKA_BROKER_URL")
kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

context = ssl.create_default_context()

producer = KafkaProducer(
    bootstrap_servers=kafka_broker.split(","),
    security_protocol="SSL",
    ssl_context=context,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

i = 0
while True:
    producer.send(
        kafka_topic,
        {
            "message": f"msg {i}",
            "time": datetime.now().isoformat()
        }
    )
    print(f"Sent {i}")
    i += 1
    time.sleep(2)