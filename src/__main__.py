from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        team4099 = Team(key="frc4099")
        print([match.actual_time.year for match in team4099.matches(year=range(2010, 2022))])

main()
