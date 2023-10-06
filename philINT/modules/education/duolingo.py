import httpx, configparser, datetime, pycountry
from iso639 import languages
from collections import namedtuple

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

DuolingoData = namedtuple("Duolingo", ["Username", "Picture", "Name", "Account_creation_date", "Country", "Streak", "Has_recent_activity", "Bio", "Languages_studied"])
Course = namedtuple("Duolingo_Course", ["Language", "Learning_from", "Crowns", "Completion", "Exp"])

def duolingo_response_parser(response):
    usercount = len(response["users"])
    match usercount:
        case 0:
            return None
        case 1:
            print("Duolingo : found 1 user.")
        case _:
            print("Duolingo : found multiple (" + str(usercount) + ") users.")
    results = [
        DuolingoData(
        Username = user["username"],
        Picture = "https:" + user["picture"] + "/xxlarge" if "default" not in user["picture"] else None,
        Name = user["name"] if "name" in user else None,
        Account_creation_date = str(datetime.datetime.fromtimestamp(user["creationDate"])),
        Country = pycountry.countries.get(alpha_2=user["profileCountry"]).name if user["profileCountry"] is not None else None,
        Streak = str(user["streak"]),
        Has_recent_activity = str(user["hasRecentActivity15"]),
        Bio = user["bio"] if user["bio"] != "" else None,
        Languages_studied = [
            Course(
                Language = course["title"],
                Learning_from = languages.get(alpha2=course["fromLanguage"]).name,
                Crowns = course["crowns"],
                Completion = str(round(100 * course["crowns"] / int(CROWN_DICT[course["title"] + "_" + languages.get(alpha2=course["fromLanguage"]).name]), 2)) + " %",
                Exp = course["xp"]
            )
            for course in user["courses"]
        ]
        )
        for user in response["users"]
    ]
    return results

async def from_email(email):
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint_config["Duolingo"]["ENDPOINT_EMAIL"] + email, headers={"User-Agent": endpoint_config["BASE"]["USER_AGENT"]})
    return duolingo_response_parser(response.json())

async def from_username(username):
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint_config["Duolingo"]["ENDPOINT_USERNAME"] + username, headers={"User-Agent": endpoint_config["BASE"]["USER_AGENT"]})
    return duolingo_response_parser(response.json())

CROWN_DICT = {'Arabic_English': '276',
 'Chinese_English': '528',
 'Czech_English': '504',
 'Danish_English': '420',
 'Dutch_English': '738',
 'Esperanto_English': '414',
 'Finnish_English': '210',
 'French_English': '1406',
 'German_English': '826',
 'Greek_English': '570',
 'Haitian Creole_English': '216',
 'Hawaiian_English': '228',
 'Hebrew_English': '504',
 'High Valyrian_English': '258',
 'Hindi_English': '192',
 'Hungarian_English': '468',
 'Indonesian_English': '414',
 'Irish_English': '384',
 'Italian_English': '396',
 'Japanese_English': '655',
 'Klingon_English': '390',
 'Korean_English': '564',
 'Latin_English': '132',
 'Navajo_English': '66',
 'Norwegian_English': '1032',
 'Polish_English': '402',
 'Portuguese_English': '546',
 'Romanian_English': '372',
 'Russian_English': '474',
 'Scottish Gaelic_English': '642',
 'Spanish_English': '1521',
 'Swahili_English': '390',
 'Swedish_English': '396',
 'Turkish_English': '402',
 'Ukrainian_English': '306',
 'Vietnamese_English': '504',
 'Welsh_English': '642',
 'Yiddish_English': '564',
 'Zulu_English': '120',
 'Catalan_Spanish': '378',
 'English_Spanish': '1439',
 'Esperanto_Spanish': '372',
 'French_Spanish': '408',
 'German_Spanish': '432',
 'Guarani_Spanish': '330',
 'Italian_Spanish': '396',
 'Portuguese_Spanish': '414',
 'Russian_Spanish': '420',
 'Swedish_Spanish': '684',
 'Cantonese_Chinese': '108',
 'English_Chinese': '882',
 'French_Chinese': '654',
 'Japanese_Chinese': '666',
 'Korean_Chinese': '894',
 'Italian_Chinese': '396',
 'Spanish_Chinese': '384',
 'English_French': '330',
 'Esperanto_French': '414',
 'German_French': '702',
 'Italian_French': '600',
 'Portuguese_French': '414',
 'Spanish_French': '456',
 'English_Portuguese': '1321',
 'Esperanto_Portuguese': '372',
 'French_Portuguese': '420',
 'German_Portuguese': '438',
 'Italian_Portuguese': '408',
 'Spanish_Portuguese': '384',
 'English_Arabic': '366',
 'French_Arabic': '468',
 'German_Arabic': '720',
 'Swedish_Arabic': '396',
 'English_German': '380',
 'French_German': '774',
 'Italian_German': '180',
 'Spanish_German': '384',
 'English_Italian': '372',
 'French_Italian': '468',
 'German_Italian': '432',
 'Spanish_Italian': '384',
 'Chinese_Japanese': '360',
 'English_Japanese': '816',
 'French_Japanese': '360',
 'Korean_Japanese': '360',
 'English_Russian': '774',
 'French_Russian': '468',
 'German_Russian': '666',
 'Spanish_Russian': '384',
 'English_Dutch': '330',
 'French_Dutch': '360',
 'German_Dutch': '468',
 'English_Turkish': '330',
 'German_Turkish': '432',
 'Russian_Turkish': '318',
 'English_Hungarian': '330',
 'German_Hungarian': '306',
 'Chinese_Vietnamese': '360',
 'English_Vietnamese': '630',
 'English_Bengali': '120',
 'English_Czech': '330',
 'English_Greek': '330',
 'English_Hindi': '324',
 'English_Indonesian': '275',
 'English_Korean': '522',
 'English_Polish': '330',
 'English_Romanian': '330',
 'English_Thai': '354',
 'English_Tagalog': '276',
 'English_Ukrainian': '330',
 'Welsh_English': '708'}