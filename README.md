# philINT

philINT is an OSINT tool and a Python 3 library that allows investigators to gather information from an email address or an username, without alerting the target.

The main difference between philINT and already existing solutions is that you are 100% sure that the tool will not gather any information about you - as you have access to all the code and run it yourself.

Features :
- Fully async with sync compatibility
- *.gpx* files visualisation
- Easy data export

## Requirements

+ [Python 3](https://www.python.org/downloads/)

## Installation

With PyPI :
```
pip install philINT
```

With GitHub :
```
git clone https://github.com/ajuelosemmanuel/philINT.git
cd philINT
python3 setup.py install
```

And then fill the `credentials.conf` file with the credentials required for some sources. Not filling it will not break the script.

## Usage

```
usage: philINT [-h] (-e EMAIL | -u USERNAME) [-x]

Script that tries to retrieve information from an email address

options:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        Target email address
  -u USERNAME, --username USERNAME
                        Target username
  -x, --extract
                        Extracts the raw data to a json file
```

### CLI Exemple

```
philINT.exe -e example.email@email.com
Duolingo : found 1 user.
Chess.com : found 1 user.
philINT - by Emmanuel Ajuelos (https://github.com/ajuelosemmanuel)
-------------------------------------
|              Results              |
-------------------------------------
Email address : example.email@email.com
         • Spam : False
         • Deliverable : True
         • Disposable : False
Email addresses :
         • example.mail@mail.com
Usernames :
         • examplema1
         • examplemail
Names :
         • Example Mail
Pictures :
         • https://simg-ssl.duolingo.com/avatars/XXXXXXXXXX/XXXXXXXXXX/xxlarge
         • https://images.chesscomfiles.com/uploads/v1/user/XXXXXXXXX.XXXXXXXX.200x200o.XXXXXXXXX.jpeg
Accounts :
         • Duolingo
         • Chess.com
```

### Python Exemple

```python
import philINT.classes

target = "exemple.email@email.com"

email = philINT.classes.Email(target)
email.run_all()
target_person = philINT.classes.Person()
target_person.fill_from_email(email)


email.display()
target_person.display()
target_person.display_raw_data()
```

## Other

Inspired by [Palenath](https://github.com/megadose)'s work, especially [holehe](https://github.com/megadose/holehe). Not knowing how to strucuture my project, I used an extremely similar one.

## Troubleshooting

The `User-Agent` might get banned - feel free to tell me about it, and I will change it.

Because of the number of sources, I can't test all of them every day. Please reach out to me if one isn't working - I'll do my best to solve the problem. Also, keep in mind that people can delete their accounts, or simply don't have one sometimes.

## False positives

Keep in my, especially when searching usernames, that multiple people can use the same username - and therefore generate false positives.

## Wanna contribute ?

Here are a few ways you can help me on this project !
### Sponsoring

Using GitHub sponsors, you can help me buy API access to some websites, such as HaveIBeenPwned, in order to create new modules for everyone to use.

### Making new modules

Here is a template for a module :

```python
import httpx, configparser
from collections import namedtuple

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

WebsiteData = namedtuple("Website", ["Data1", "Data2", "Data3", "DataETC"])

async def from_email(email):
    headers = {"User-Agent": endpoint_config["BASE"]["USER_AGENT"]}
    json = {}
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint_config["Website"]["ENDPOINT_EMAIL"], headers = headers, json = json)
    resp = response.json()
    results = WebsiteData(
        Data1 = None,
        Data2 = None,
        Data3 = None,
        DataETC = None
        )
    return results
```

You need to do the parsing, etc

For web scraping, I use Selenium, and all the code is async compatible - with non-async aliases when possible.

## Licence

[GNU GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Disclaimer

**Use philINT ONLY in personal or criminal investigations, pentesting or open-source projects. I'm not responsible of its use, and the project was made for educational purposes only.**

## Modules

| Source      | Domain          | Email | Username |
| ----------- | --------------- | ----- | -------- |
| Adobe       | adobe.com       | ✓    | ✗       |
| Chess.com   | chess.com       | ✓    | ✓       |
| Duolingo    | duolingo.com    | ✓    | ✓       |
| GitHub      | github.com      | ✓    | ✓       |
| Gravatar    | gravatar.com    | ✓    | ✗       |
| Imgur       | imgur.com       | ✓    | ✗       |
| MeWe        | mewe.com        | ✓    | ✗       |
| MyAnimeList | myanimelist.net | ✗    | ✓       |
| Twitter     | twitter.com     | ✓    | ✗       |
| WordPress   | wordpress.com   | ✓    | ✗       |
