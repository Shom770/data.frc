import asyncio

from api_client import *


async def main():
    api_client = ApiClient()

    print(await api_client.teams(page_num=1, year=range(2020, 2022), simple=True))

asyncio.run(main())
