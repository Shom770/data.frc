import asyncio

from api_client import *


def main():
    api_client = ApiClient()

    print(api_client.teams(year=2022, simple=True))

main()