from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(Team(key="frc4099").robots())


main()
