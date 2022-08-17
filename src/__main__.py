from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(District(key="2022chs").events(keys=True)[0])


main()
