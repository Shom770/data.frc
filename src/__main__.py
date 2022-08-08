from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        var: Match = Team(key="frc4099").events(year=2022)[0]
        print(var)

main()
