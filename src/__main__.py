from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(Team(key="frc2363").events(year=2022, statuses=True))


main()
