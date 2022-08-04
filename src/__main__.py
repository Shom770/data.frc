from api_client import *


def main():
    with ApiClient(persistent_session=True) as api_client:
        print(api_client.teams(year=2022, simple=True))


main()
