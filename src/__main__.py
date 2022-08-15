from api_client import *
from schemas import *


def main():
    with ApiClient():
        ranks = Event(key="2022chcmp").district_points()
        print(dict(sorted(ranks.points.items(), key=lambda x: x[1]["total"])))


main()
