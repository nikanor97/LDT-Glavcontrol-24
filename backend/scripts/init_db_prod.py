import asyncio
import random
import uuid
from decimal import Decimal

import uvloop
from fastapi import UploadFile
from loguru import logger

import settings
from common.rabbitmq.connection_pool import ConnectionPool as AmqpConnectionPool
from common.rabbitmq.publisher import Publisher
from src.db.main_db_manager import MainDbManager
from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.db_manager.application_product import ApplicationProductDbManager
from src.db.projects.db_manager.company import CompanyDbManager
from src.db.projects.db_manager.forecast import ForecastDbManager
from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.db.projects.db_manager.product import ProductDbManager
from src.db.projects.db_manager.remains import RemainsDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.application_product import ApplicationProduct
from src.db.projects.models.company import Company
from faker import Faker

from src.db.projects.models.forecast import Forecast
from src.db.projects.models.procurement import Procurement
from src.db.projects.models.product import Product
from src.db.projects.models.remains import Remains
from src.db.projects.models.user_company import UserCompany
from src.db.users.db_manager.user import UserDbManager
from src.db.users.db_manager.user_password import UserPasswordDbManager
from src.db.users.models.user import User

fake = Faker()


lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed elit ligula, gravida sed hendrerit sed, congue ut justo. Pellentesque vel volutpat dolor. Vivamus vestibulum, arcu mattis sollicitudin luctus, nunc ante convallis elit, vel fringilla orci est at sapien. Etiam a ultricies turpis. Duis ac libero eget urna tincidunt scelerisque. Maecenas in elementum ipsum. In vitae lacus in ligula molestie porta nec id lectus. Proin ac purus feugiat, suscipit felis sed, convallis mi. Suspendisse potenti. Sed imperdiet bibendum mattis. Sed id elementum lectus, id suscipit libero. In hac habitasse platea dictumst. Proin eget tellus lobortis elit euismod tempus sit amet sed enim. Integer a euismod nunc. Vivamus consectetur sollicitudin lacus, et tristique metus semper in. Donec rhoncus aliquet quam ut semper. Proin congue, nibh quis suscipit placerat, est tellus egestas augue, non fermentum risus neque sit amet purus. Maecenas ultricies interdum sagittis. Suspendisse et neque erat. Vestibulum maximus, ante et cursus commodo, ipsum est mattis diam, vitae dignissim tellus ipsum molestie nibh. Sed vel odio consequat, rutrum massa non, tristique erat. Sed in pulvinar tortor. Aliquam et sodales ex. Vivamus urna leo, aliquam at felis eu, luctus pretium est. Fusce vitae ultrices diam, nec egestas elit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Duis at volutpat magna. Duis vel blandit ex, et cursus odio. Nunc dictum porta accumsan. Aenean at sapien elit. Sed felis massa, molestie eu vehicula tincidunt, sodales at dolor. Nullam ut vulputate magna, sed consectetur leo. Vivamus vitae augue et erat tempus suscipit quis pellentesque augue. Quisque malesuada scelerisque mi, at sollicitudin ipsum condimentum eu. Duis fermentum tempor sollicitudin. Cras lacinia et erat in egestas. Aenean vitae neque nec odio accumsan porttitor. In hac habitasse platea dictumst. Nam vestibulum lobortis erat quis dignissim. Cras congue justo mi, id efficitur neque rutrum vitae. Nullam non eleifend magna, sed placerat purus. Donec bibendum purus malesuada risus tempor, vitae pellentesque purus faucibus. Donec nec nunc neque. Cras quis hendrerit tellus, posuere volutpat turpis. Sed et dolor sem. Praesent non dapibus est. Suspendisse et sagittis nisl. Duis posuere luctus consequat. Proin dignissim tempus felis ut semper. Vivamus mauris metus, efficitur dapibus interdum vitae, tempor vel velit. In tempus libero massa, sit amet porttitor nisi congue imperdiet. Vivamus in diam sed massa efficitur fermentum. Sed turpis justo, sagittis non volutpat eget, posuere quis lectus. Aliquam eget magna magna. Aenean nec nulla lacus."""
colors = ['#00C12B', '#510FAE', '#FF7400']
houses = [
    'Верейская 41',
    "Квартал Строгино",
    "Квартал Ивакино",
    "Польские Кварталы",
    "Квартал Марьино",
    "Новое Видное",
    "Пятницкие Луга",
    "Пригород Лесное",
    "Квартал Западный",
    "Рублевский Квартал",
]

@logger.catch()
async def init_db():
    main_db_manager = MainDbManager(db_name_prefix=settings.DB_NAME_PREFIX)

    # amqp_connection_pool = AmqpConnectionPool(
    #     login=settings.RABBIT_LOGIN,
    #     password=settings.RABBIT_PASSWORD,
    #     host=settings.RABBIT_HOST,
    #     port=settings.RABBIT_PORT,
    #     ssl=settings.RABBIT_SSL,
    #     no_verify_ssl=True,
    # )
    #
    # publisher = Publisher(
    #     connection_pool=amqp_connection_pool,
    # )

    async with main_db_manager.users.make_autobegin_session() as session:
        admin_users_raw = [User(
            name=fake.name(),
            email=fake.email(),
            permission_read_stat=bool(random.getrandbits(1)),
            permission_create_order=bool(random.getrandbits(1)),
            is_deleted=False,
            role="admin",
            telegram_username=fake.user_name()
        ) for _ in range(10)]

        regular_users_raw = [User(
            name=fake.name(),
            email=fake.email(),
            permission_read_stat=bool(random.getrandbits(1)),
            permission_create_order=bool(random.getrandbits(1)),
            is_deleted=False,
            role="user",
            telegram_username=fake.user_name()
        ) for _ in range(25)]

        custom_admin_user_raw = User(
            name="admin",
            email="admin@mail.ru",
            permission_read_stat=True,
            permission_create_order=True,
            is_deleted=False,
            role="admin",
            telegram_username=fake.user_name()
        )
        admin_users_raw.append(custom_admin_user_raw)
        custom_regular_user_raw = User(
            name="regular_user",
            email="user@mail.ru",
            permission_read_stat=True,
            permission_create_order=True,
            is_deleted=False,
            role="user",
            telegram_username=fake.user_name()
        )
        regular_users_raw.append(custom_regular_user_raw)

        admin_users: list[User] = []
        regular_users: list[User] = []
        for user in admin_users_raw:
            admin_users.append(await UserDbManager.create_user(session, user))
        for user in regular_users_raw:
            regular_users.append(await UserDbManager.create_user(session, user))

        for user in admin_users + regular_users:
            await UserPasswordDbManager.create_user_password(session, user.id, "test")

    async with (main_db_manager.projects.make_autobegin_session() as session):
        companies_raw = [Company(
            name=fake.company(),
            region=fake.city(),
            inn=str(fake.random_int(min=1000000000, max=9999999999)),
            ogrn=str(fake.random_int(min=1000000000000, max=9999999999999)),
            director=fake.name(),
            foundation_date=fake.date_of_birth(minimum_age=4, maximum_age=100),
        ) for _ in range(15)]

        companies: list[Company] = []
        for comp in companies_raw:
            companies.append(await CompanyDbManager.create_company(session, comp))

        user_companies_raw = [UserCompany(
            user_id=user.id,
            company_id=random.choice(companies).id
        ) for user in regular_users + admin_users]

        user_companies: list[UserCompany] = []
        for uc in user_companies_raw:
            user_companies.append(await UserCompanyDbManager.create_user_company(session, uc))

        applications = [Application(
            calculation_id=str(uuid.uuid4()),
            lot_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            shipment_start_date=fake.date_of_birth(minimum_age=0, maximum_age=4),
            shipment_end_date=fake.date_of_birth(minimum_age=0, maximum_age=4),
            shipment_volume=random.randint(100, 1000),
            shipment_address=fake.address(),
            shipment_terms=fake.sentence(),
            year=random.randint(2020, 2024),
            gar_id=str(uuid.uuid4()),
            spgz_end_id=str(uuid.uuid4()),
            amount=Decimal(random.randint(10000, 100000) * random.random()),
            unit_of_measurement=fake.word(),
            author_id=random.choice(regular_users).id,
            status="draft"
        ) for _ in range(100)]

        for application in applications:
            await ApplicationDbManager.create_application(session, application)

        products_raw = [Product(
            name=fake.word(),
            price=Decimal(random.randint(100, 1000) * random.random()),
            number=random.randint(1, 100),
            amount=Decimal(random.randint(10000, 100000) * random.random())
        ) for _ in range(500)]

        products = await ProductDbManager.create_products(session, products_raw)

        await session.flush()

        application_products_raw: list[ApplicationProduct] = []

        for i in range(3):
            application_products_raw.extend([ApplicationProduct(
                application_id=a.id,
                product_id=products[idx + i * len(applications)].id
            ) for idx, a in enumerate(applications)])

        application_products = await ApplicationProductDbManager.create_application_products(
            session, application_products_raw
        )

        remains_raw = [Remains(
            cmo=fake.word(),
            koc=random.randint(1, 100),
            number=random.randint(1, 100),
            indicator=random.randint(1, 100),
            saldo_begin_debet=Decimal(random.randint(10000, 100000) * random.random()),
            saldo_begin_credit=Decimal(random.randint(10000, 100000) * random.random()),
            saldo_period_debet=Decimal(random.randint(10000, 100000) * random.random()),
            saldo_period_credit=Decimal(random.randint(10000, 100000) * random.random()),
            saldo_end_debet=Decimal(random.randint(10000, 100000) * random.random()),
            saldo_end_credit=Decimal(random.randint(10000, 100000) * random.random()),
            product_id=random.choice(products).id
        ) for _ in range(100)]

        remains: list[Remains] = []
        for r in remains_raw:
            remains.append(await RemainsDbManager.create_remains(session, r))

        forecasts_raw: list[Forecast] = []
        for i in range(20):
            forecasts_raw.extend([Forecast(
            product_id=p.id,
            quarter=random.randint(1, 50),
            year=random.randint(2020, 2024)
        ) for p in products])

        forecasts: list[Forecast] = []
        for f in forecasts_raw:
            forecasts.append(await ForecastDbManager.create_forecast(session, f))

        procurements_raw = [Procurement(
            spgz_id=str(uuid.uuid4()),
            spgz_name=fake.word(),
            procurement_date=fake.date_of_birth(minimum_age=0, maximum_age=4),
            price=Decimal(random.randint(10000, 100000) * random.random()),
            way_to_define_supplier=fake.word(),
            contract_basis=fake.word()
        ) for _ in range(500)]

        procurements = await ProcurementDbManager.create_procurements(session, procurements_raw)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        app = loop.run_until_complete(init_db())
    finally:
        loop.close()
