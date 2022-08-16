from api_client import *
from schemas import *


def main():
    with ApiClient():
        ranks = Team(key="frc4099").events()
        print(ranks)


main()
