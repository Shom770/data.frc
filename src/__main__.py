import functools

from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(api_client.events(year=range(2019, 2023), simple=True)[0])


main()
