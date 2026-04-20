from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import json
import os
from datetime import datetime
import time

kafka_broker = os.environ.get("KAFKA_BROKER_URL")
kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

# ✅ Create topic (safe retry)
try:
    admin = KafkaAdminClient(
        bootstrap_servers=kafka_broker.split(","),
        security_protocol="SSL",
        client_id="admin-client"
    )

    topic_list = [
        NewTopic(name=kafka_topic, num_partitions=1, replication_factor=2)
    ]

    admin.create_topics(new_topics=topic_list, validate_only=False)
    print("✅ Topic created")

except Exception as e:
    print(f"⚠️ Topic may already exist: {e}")

# ✅ Producer
producer = KafkaProducer(
    bootstrap_servers=kafka_broker.split(","),
    security_protocol="SSL",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print("🚀 Producer started...")

i = 0
while True:
    producer.send(
        kafka_topic,
        {
            "message": f"msg {i}",
            "time": datetime.now().isoformat()
        }
    )

    producer.flush()   # ✅ important

    print(f"Sent {i}")
    i += 1
    time.sleep(2)