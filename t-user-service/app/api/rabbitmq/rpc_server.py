import logging
import os
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from .. import auth_handler

RABBITMQ_URL = os.getenv('RABBITMQ_URL')


async def start_listening() -> None:
    # Perform connection
    connection = await connect(RABBITMQ_URL)

    # Creating a channel
    channel = await connection.channel()
    exchange = channel.default_exchange

    # Declaring queue
    queue = await channel.declare_queue("rpc_queue")

    print(" [x] Awaiting RPC requests")

    # Start listening the queue with name 'hello'
    async with queue.iterator() as qiterator:
        message: AbstractIncomingMessage
        async for message in qiterator:
            try:
                async with message.process(requeue=False):
                    assert message.reply_to is not None
                    token = str(message.body.decode())
                    userId = (await auth_handler.get_current_user(token)).id
                    response = str(userId).encode()
                    await exchange.publish(
                        Message(
                            body=response,
                            correlation_id=message.correlation_id,
                        ),
                        routing_key=message.reply_to,
                    )
            except Exception:
                logging.exception("Processing error for message %r", message)
