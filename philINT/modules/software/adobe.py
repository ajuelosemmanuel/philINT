import httpx, configparser
from collections import namedtuple

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

AdobeData = namedtuple("Adobe", ["Linked_to_Google", "Linked_to_Facebook", "is_Active", "Pictures"])

async def from_email(email):
    headers = {"User-Agent": endpoint_config["BASE"]["USER_AGENT"], "content-type": "application/json","x-ims-clientid": "adobedotcom2"}
    json = {"username": email}
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint_config["Adobe"]["ENDPOINT_EMAIL"], headers = headers, json = json)
    resp = response.json()
    usercount = len(resp)
    match usercount:
        case 0:
            return None
        case 1:
            print("Adobe : found 1 user.")
        case _:
            print("Adobe : found multiple (" + str(usercount) + ") users.")
    results = [
        AdobeData(
        Linked_to_Google = "google" in str(el["authenticationMethods"]),
        Linked_to_Facebook = "facebook" in str(el["authenticationMethods"]),
        is_Active = el["status"]["code"],
        Pictures = el["images"]
        )
        for el in resp
    ]
    return results