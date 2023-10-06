import httpx, configparser
from collections import namedtuple

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

ImgurData = namedtuple("Imgur", ["Has_account"])

async def from_email(email):
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": endpoint_config["BASE"]["USER_AGENT"]
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(endpoint_config["Imgur"]["ENDPOINT_EMAIL"], headers = headers, data = "email=" + email)
    response = resp.json()
    if "data" in response and response["data"]["available"] == False:
        print("Imgur : found 1 user.")
        return ImgurData(Has_account = True)
    return None