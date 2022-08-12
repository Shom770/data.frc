import functools

from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        team4099 = Team(key="frc254")
        print(team4099.media(year=range(2020, 2023), media_tag="youtube"))


main()
