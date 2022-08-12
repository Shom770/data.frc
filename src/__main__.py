import functools

from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        team4099 = Team(key="frc4099")
        print(team4099.social_media())


main()
