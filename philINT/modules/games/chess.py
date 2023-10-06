import httpx, configparser, datetime, time
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

endpoint_config = configparser.ConfigParser()
endpoint_config.read('philINT/endpoints.conf')

credentials_config = configparser.ConfigParser()
credentials_config.read('philINT/credentials.conf')

ChessData = namedtuple("Chess", ["Picture", "Profile", "Name", "Username", "Country", "Location", "Last_online", "Account_creation_date"])

async def from_email(email):
    username = credentials_config["Chess"]["USERNAME"]
    password = credentials_config["Chess"]["PASSWORD"]
    if username == '' or password == '':
        return None
    options = Options()
    options.add_argument('--headless=new')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.chess.com/login")
    driver.find_element("id", "username").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    driver.find_element("id", "login").click()
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    driver.get("https://www.chess.com/friends?name=" + email)
    time.sleep(0.18)
    try :
        driver.find_element(By.CLASS_NAME, "friends-section-suggestions")
    except NoSuchElementException :
        return None
    user_data = driver.find_element(By.CLASS_NAME, "users-list-item")
    user_data.get_attribute("innerHTML")
    return await from_username(user_data.get_attribute("innerHTML").split("username")[1].split("\"")[1])

async def from_username(username):
    async with httpx.AsyncClient() as client:
        resp = await client.get(endpoint_config["Chess"]["ENDPOINT_USERNAME"] + username.lower(), headers={"User-Agent": endpoint_config["BASE"]["USER_AGENT"]})
    if 'not found' in resp.text or resp.text == "":
        return None
    print("Chess.com : found 1 user.")
    response = resp.json()
    return ChessData(
        Picture = response["avatar"] if "avatar" in response else None,
        Profile = response["url"],
        Name = response["name"] if "name" in response else None,
        Username = response["username"],
        Country = response["country"],
        Location = response["location"] if "location" in response else None,
        Last_online = datetime.datetime.utcfromtimestamp(response["last_online"]).strftime('%Y-%m-%d %H:%M:%S'),
        Account_creation_date = datetime.datetime.utcfromtimestamp(response["joined"]).strftime('%Y-%m-%d %H:%M:%S')
    )