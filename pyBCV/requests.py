import requests
from requests import Response

requests.packages.urllib3.disable_warnings()


def ensure_200_response_and_return_content(response: Response):
    if not response.status_code == requests.codes.ok:
        raise ValueError("Unsuccessful communication with BCV server.")

    return response.content


class BCVRequests:
    TASAS_INFORMATIVAS_URL = (
        "https://www.bcv.org.ve/tasas-informativas-sistema-bancario"
    )
    MAIN_URL = "https://www.bcv.org.ve/"

    @classmethod
    def get_main_page(cls):
        return ensure_200_response_and_return_content(
            requests.get(cls.MAIN_URL, verify=False)
        )

    @classmethod
    def get_tasas_bancos(cls):
        return ensure_200_response_and_return_content(
            requests.get(cls.TASAS_INFORMATIVAS_URL, verify=False)
        )
