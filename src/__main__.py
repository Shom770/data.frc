from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        var: Match = Team(key="frc4099").robots()
        print(var)

main()
