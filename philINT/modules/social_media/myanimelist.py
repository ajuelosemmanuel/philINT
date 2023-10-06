import httpx, configparser
from collections import namedtuple

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

MyAnimeListData = namedtuple("MyAnimeList", ["Last_online", "Gender", "Date_of_birth", "Location", "Joined_at"], defaults=(None,) * 5)

async def from_username(username):
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint_config["MyAnimeList"]["ENDPOINT_USERNAME"] + username, headers={"User-Agent": endpoint_config["BASE"]["USER_AGENT"]})
    if response.status_code == 404:
        return None
    print("MyAnimeList : found 1 user.")
    parsed = response.text.split("user-status border-top")[1].split("</ul>")[0].split('<span class="user-status-title di-ib fl-l fw-b">')[1:]
    results = MyAnimeListData()
    for line in parsed:
        parsed_line = line.split('</span><span class="user-status-data di-ib fl-r">')
        match parsed_line[0]:
            case 'Last Online':
                results = results._replace(Last_online=parsed_line[1].split("</span>")[0])
            case 'Gender':
                results = results._replace(Gender=parsed_line[1].split("</span>")[0])
            case 'Birthday':
                results = results._replace(Date_of_birth=parsed_line[1].split("</span>")[0])
            case 'Location':
                results = results._replace(Location=parsed_line[1].split("</span>")[0])
            case 'Joined':
                results = results._replace(Joined_at=parsed_line[1].split("</span>")[0])
    return results