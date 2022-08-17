from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(api_client.match("2022cmptx_f1m1"))


main()
