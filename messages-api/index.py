import os
import ydb

endpoint = os.getenv("YDB_ENDPOINT")
database = os.getenv("YDB_DATABASE")
auth_token = os.getenv("IAM_TOKEN")


async def fetch_rows_from_messages_table_async(pool: ydb.aio.QuerySessionPool):
    print("Fetching rows from messages table...")
    result_sets = await pool.execute_with_retries(
        """
        select text from messages;
        """
    )
    return result_sets[0].rows


async def get_messages():
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
            messages = await fetch_rows_from_messages_table_async(pool)
            return messages


async def handler(event, context):
    messages = await get_messages()
    return {
        'statusCode': 200,
        'body': messages,
    }
