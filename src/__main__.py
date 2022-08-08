from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        var: Match = Team(key="frc4099").event("2022chcmp", matches=True, simple=True)[0]
        print(var.alliances)


main()
