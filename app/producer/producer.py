import os
from kafka import KafkaProducer
from datetime import datetime
import json
import time

kafka_broker = os.environ.get("KAFKA_BROKER_URL")
kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

producer = KafkaProducer(
    bootstrap_servers=[kafka_broker],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

i = 0
while True:  # 🔥 continuous producer
    producer.send(
        kafka_topic,
        {
            "sender": "buildingminds",
            "content": f"message {i}",
            "created_at": datetime.now().isoformat(),
        },
    )
    print(f"message {i} sent")
    i += 1
    time.sleep(0.2)  # fast producer