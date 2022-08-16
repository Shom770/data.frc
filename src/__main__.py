from api_client import *
from schemas import *


def main():
    with ApiClient():
        ranks = Event(key="2022chcmp").matches(simple=True)[0].alliances
        print(ranks)


main()
