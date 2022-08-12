import functools

from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(api_client.event(event_key="2022aowuer"))


main()
