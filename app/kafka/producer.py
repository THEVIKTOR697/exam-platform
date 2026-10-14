from aiokafka import AIOKafkaProducer
import json


class KafkaProducer:

    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers="kafka:9092"
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, event):
        await self.producer.send_and_wait(
            topic,
            json.dumps(event).encode("utf-8")
        )
