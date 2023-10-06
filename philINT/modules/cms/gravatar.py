import httpx, configparser, hashlib
from collections import namedtuple

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

GravatarData = namedtuple("Gravatar", ["Profile", "Username", "Picture", "Pictures", "Name", "Display_name", "About_me", "Accounts", "Currency", "URLs"])
LinkedAccount = namedtuple("Gravatar_Linked_Account", ["Domain", "Display_name", "URL", "Username", "Website_name"])
Currency = namedtuple("Gravatar_Currency", ["Type", "Wallet"])

async def from_email(email):
    email_md5 = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    async with httpx.AsyncClient() as client:
        resp = await client.get(endpoint_config["Gravatar"]["ENDPOINT_EMAIL"] + email_md5 + ".json", headers={"User-Agent": endpoint_config["BASE"]["USER_AGENT"]})
    response = resp.json()
    if "User not found" in str(response):
        return None
    usercount = len(response["entry"])
    match usercount:
        case 0:
            return None
        case 1:
            print("Gravatar : found 1 user.")
        case _:
            print("Gravatar : found multiple (" + str(usercount) + ") users.")
    return [
        GravatarData(
            Profile = el["profileUrl"],
            Username = el["preferredUsername"],
            Picture = el["thumbnailUrl"],
            Pictures = [photo["value"] for photo in el["photos"]],
            Name = el["name"]["formatted"] if "name" in el else None,
            Display_name = el["displayName"],
            About_me = el["aboutMe"] if "aboutMe" in el else None,
            Accounts = [
                LinkedAccount(
                    Domain = account['domain'],
                    Display_name = account["display"],
                    URL = account["url"],
                    Username = account["username"],
                    Website_name = account["name"]
                ) for account in el["accounts"]
            ] if "accounts" in el else None,
            Currency = [
                Currency(
                    Type = curr["type"],
                    Wallet = curr["value"]
                ) for curr in el["currency"]
            ] if "currency" in el else None,
            URLs = [url["value"] for url in el["urls"]] if len(el["urls"]) != 0 else None
        )
        for el in response["entry"]
    ]