import functools

from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(Event(key="2022iri").rankings())


main()
