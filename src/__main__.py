from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(Team(key="frc0").events(year=2029))


main()
