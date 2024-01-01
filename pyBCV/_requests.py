import requests

requests.packages.urllib3.disable_warnings()

def _ensure_200_response(url: str) -> requests.Response:
    response = requests.get(url, verify=False)
    response.raise_for_status()

    return response