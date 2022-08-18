from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(api_client.districts(year=2022))


main()
