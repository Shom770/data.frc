from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(api_client.districts(2021))


main()
