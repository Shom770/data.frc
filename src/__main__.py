from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(api_client.team("frc4099", simple=True).event("2022chcmp", status=True).qual.ranking.sort_orders)


main()
