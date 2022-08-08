from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        var: Event = Team(key="frc4099").events(year=2022)[0]

main()
