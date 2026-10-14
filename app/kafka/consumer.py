
import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

log = logging.getLogger(__name__)

TOPIC = "purchase.completed"
GROUP_ID = "exam-access-service"

async def consume():
    consumer = AIOKafkaConsumer(
        "purchase.completed",
        bootstrap_servers="kafka:9092",
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
    )

    started = False

    try:
        delay = 1

        while not started:
            try:
                await consumer.start()
                started = True
                log.info("KAFKACONSUMER: connected")

            except KafkaConnectionError:
                log.exception(
                    "KAFKACONSUMER: connection failed; "
                    "retrying in %s seconds",
                    delay,
                )

                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)

        async for message in consumer:
            try:
                event = json.loads(message.value.decode("utf-8"))

                purchase_id = event["purchase_id"]
                user_id = event["user_id"]
                exam_id = event["exam_id"]

                log.info(
                    "Processing purchase=%s user=%s exam=%s",
                    purchase_id,
                    user_id,
                    exam_id,
                )

                log.info('TODO: SEND EMAIL TO USER WITH ACCESS DETAILS. GRANT AUTHORIZATION TO USER FOR EXAM ACCESS.')

                # TODO:
                # 1. Crear una sesión de base de datos.
                # 2. Comprobar si ya existe el acceso.
                # 3. Crear el acceso si todavía no existe.
                # 4. Confirmar la transacción de base de datos.

            except Exception:
                log.exception(
                    "KAFKACONSUMER: failed to process message"
                )
                raise

    finally:
        if started:
            await consumer.stop()
            log.info("KAFKACONSUMER: stopped")


if __name__ == "__main__":
    asyncio.run(consume())
