from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(Team(key="frc4099").events(year=2022, statuses=True)[0].qual.ranking.sort_orders)


main()
