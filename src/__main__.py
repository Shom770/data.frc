from api_client import *
from schemas import *


def main():
    with ApiClient():
        ranks = Team(key="frc4099").events(year=2022, statuses=True)
        print(ranks)


main()
