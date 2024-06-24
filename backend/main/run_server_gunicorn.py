import asyncio

import uvloop

import settings
from common.rabbitmq import consumer
from common.rabbitmq.consumer import Consumer
from common.rabbitmq.publisher import Publisher
from scripts.init_db_users_only import init_db
from src.db.base_manager import run_migrations
from src.db.main_db_manager import MainDbManager
from src.server.server import make_server_app
from common.rabbitmq.connection_pool import ConnectionPool as AmqpConnectionPool
from src.server.amqp import Server as AMQPServer



def main():
    run_migrations()

    main_db_manager = MainDbManager(db_name_prefix=settings.DB_NAME_PREFIX)

    amqp_connection_pool = AmqpConnectionPool(
        login=settings.RABBIT_LOGIN,
        password=settings.RABBIT_PASSWORD,
        host=settings.RABBIT_HOST,
        port=settings.RABBIT_PORT,
        ssl=settings.RABBIT_SSL,
        no_verify_ssl=True,
    )
    #

    publisher = Publisher(
        connection_pool=amqp_connection_pool,
    )

    amqp_server = AMQPServer(
        main_db_manager=main_db_manager,
        publisher=publisher
    )
    #
    consumer = Consumer(
        connection_pool=amqp_connection_pool,
        subscriptions=amqp_server.subscriptions,
    )

    server_app = make_server_app(
        main_db_manager=main_db_manager,
        startup_events=[consumer.start],
        shutdown_events=[
            amqp_connection_pool.close,
            main_db_manager.close,
        ],
        publisher=publisher
    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(init_db())
    finally:
        loop.close()

    return server_app


app = main()
