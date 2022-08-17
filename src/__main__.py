from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(District(key="1990chs").events(simple=True))


main()
