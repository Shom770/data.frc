from api_client import *


def main():
    with ApiClient(persistent_session=True) as api_client:
        print(api_client.teams(year=range(2016, 2018), page_num=1, simple=True))


main()
