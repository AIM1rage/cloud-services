import os
import ydb

endpoint = os.getenv("YDB_ENDPOINT")
database = os.getenv("YDB_DATABASE")
auth_token = os.getenv("IAM_TOKEN")


async def create_messages_table_async(pool: ydb.aio.QuerySessionPool):
    print("Creating table messages...")
    await pool.execute_with_retries(
        """
        create table if not exists messages (
            message_id Uuid,
            text Utf8 not null,

            primary key (message_id)
        );
        """
    )


async def insert_rows_into_messages_table_async(pool: ydb.aio.QuerySessionPool):
    print("Inserting rows into messages table...")
    await pool.execute_with_retries(
        '''
        replace into messages (message_id, text)
        values
            (cast("068c9363-e341-482e-99c7-9a19d22bdf6b" as Uuid), "Да. Под прохождением курса я подразумевал именно выполнение всех заданий. И указал дату, чтобы вам успели выдать сертификат."),
            (cast("ff6d4285-a531-4d29-9621-98cc099631b7" as Uuid), "Привет! В Telegram можно отправить отложенное сообщение, которое будет доставлено в удобное для получателя время. Отправлять сообщения в 2 часа ночи, если ты прямо сейчас не общаешься с человеком — плохой тон."),
            (cast("af6d4285-a531-4d29-9621-98cc099631b7" as Uuid), "Нет, но можно скинуть и то, и другое в январе"),
            (cast("af6d4285-b324-4d29-9621-98cc099631b7" as Uuid), "А если сертификат получил, эту форму все равно ж заполнить надо, там в конце ссылку на сертификат приложить можно"),
            (cast("f4442961-412a-407f-aa71-c5458bba883f" as Uuid), "Всех с наступающим Новым Годом! Пусть он принесет новые знания и сертификаты 🎉🎄");
        '''
    )


async def create_messages():
    driver_config = ydb.DriverConfig(
        endpoint,
        database,
        credentials=ydb.AuthTokenCredentials(auth_token),
        root_certificates=ydb.load_ydb_root_certificate(),
    )
    async with ydb.aio.Driver(driver_config) as driver:
        try:
            await driver.wait(timeout=5)
        except TimeoutError:
            print("Connect failed to YDB")
            print("Last reported errors by discovery:")
            print(driver.discovery_debug_details())
            exit(1)
        async with ydb.aio.QuerySessionPool(driver) as pool:
            await create_messages_table_async(pool)
            await insert_rows_into_messages_table_async(pool)


async def handler(event, context):
    await create_messages()
    return {
        'statusCode': 201,
        'body': "Messages table created!",
    }
