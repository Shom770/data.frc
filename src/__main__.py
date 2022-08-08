from api_client import *
from schemas import *


def main():
    with ApiClient() as api_client:
        print(Team(key="frc254").event("2022cmptx", awards=True)[0].recipient_list)


main()
