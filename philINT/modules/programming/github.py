import httpx, configparser, philINT.utils
from collections import namedtuple

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

GitHubData = namedtuple("GitHub", ["Username", "Github_profile", "Github_gists_profile", "Picture", "Pictures", "Links", "Emails", "Gravatar_id", "Company", "Location", "Twitter_username", "Created_at", "Updated_at"])

async def from_email(email):
    async with httpx.AsyncClient() as client:
        resp = await client.get(endpoint_config["GitHub"]["ENDPOINT_EMAIL"] + email)
    response = resp.json()
    if response["total_count"] == 1:
        return await from_username(response["items"][0]["login"])
    elif response["total_count"] == 0:
        return None
    else:
        print("GitHub : Multiple users display the same email address, can't pivot accurately")
        return None

async def username_to_readme(username):
    async with httpx.AsyncClient() as client:
        resp = await client.get(endpoint_config["GitHub"]["ENDPOINT_USERNAME"] + username + "/repos")
    repos = resp.json()
    if repos != []:
        for el in repos:
            if el["url"].endswith(username):
                async with httpx.AsyncClient() as client:
                    return await client.get("https://raw.githubusercontent.com/" + username + "/" + username + "/master/README.md").text
    return None

async def from_username(username):
    async with httpx.AsyncClient() as client:
        resp = await client.get(endpoint_config["GitHub"]["ENDPOINT_USERNAME"] + username)
    user_data = resp.json()
    if "message" in user_data:
        return None
    print("GitHub : found 1 user.")
    readme = await username_to_readme(username)
    if readme is not None :
        readme_data = philINT.utils.extract_links_and_emails(readme)
    else:
        readme_data = None
    return GitHubData(
        Username = user_data["login"],
        Github_profile = user_data["html_url"],
        Github_gists_profile = user_data["html_url"][0:8] + "gists." + user_data["html_url"][8:] if user_data["public_gists"] != 0 else None,
        Picture = user_data["avatar_url"],
        Pictures = readme_data[1] if readme_data is not None and readme_data[1] != [] else None,
        Links = readme_data[0] + [user_data["blog"]] if readme_data is not None and readme_data[0] != [] and user_data["blog"] != [] else [user_data["blog"]] if user_data["blog"] != "" else readme_data[0] if readme_data is not None and readme_data[0] != [] else None,
        Emails = readme_data[2] + [user_data["email"]] if readme_data is not None and readme_data[2] != [] and user_data["email"] != [] else [user_data["email"]] if user_data["email"] != "" else readme_data[2] if readme_data is not None and readme_data[2] != [] else None,
        Gravatar_id = user_data["gravatar_id"] if user_data["gravatar_id"] != "" else None,
        Company = user_data["company"] if user_data["company"] != "" else None,
        Location = user_data["location"] if user_data["location"] != "" else None,
        Twitter_username = user_data["twitter_username"] if user_data["twitter_username"] != "" else None,
        Created_at = user_data["created_at"],
        Updated_at = user_data["updated_at"]
    )
