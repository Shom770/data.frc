from api_client import *
from schemas import *


def main():
    with ApiClient():
        ranks = Event(key="2022chcmp").teams(statuses=True)["frc4099"].playoff
        print(ranks)


main()
