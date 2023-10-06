import re, pkgutil, importlib, asyncio, json, datetime, gpxpy, httpx, folium, pandas

# Some patterns that are useful
REGEX_EMAIL_CHECK = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
REGEX_IMAGE_LINK = re.compile(r"(http)?s?:?(\/\/[^\"']*\.(?:png|jpg|jpeg|gif|png|svg))")
REGEX_LINK = re.compile(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")

def data_cleaner(connections:list[list[object]]) -> list[object]:
    """
    Turns a list of list of connections to a list of connections
    """
    res = []
    for el in connections:
        if type(el) == list and len(el) == 1:
            res.append(el[0])
        elif type(el) == list and len(el) > 1:
            for elem in el:
                res.append(elem)
        else:
            res.append(el)
    return res

def is_email(input:str) -> bool:
    """
    Checks if a string is an email address
    """
    return bool(re.fullmatch(REGEX_EMAIL_CHECK, input))

def dot_at_converter(text:str) -> str:
    """
    Replaces some of the other ways to design a dot, in order to find email addresses in a string.
    """
    return text.replace(' [dot] ', ".").replace('[dot]', ".").replace(' (dot) ', ".").replace('(dot)', ".").replace('dot', ".").replace(' [at] ', ".").replace('[at]', ".").replace(' (at) ', ".").replace('(at)', ".").replace('at', ".")

def extract_links_and_emails(text:str) -> tuple[list]:
    """
    Get all links, images and email addresses from a string.
    Output is a tuple of 3 lists.
    """
    text_processed = dot_at_converter(text)
    links_images = re.findall(REGEX_IMAGE_LINK, text_processed)
    clean_links_images = list(set([(el[0] + "s:" + el[1]).lower() for el in links_images]))
    text_processed = re.sub(REGEX_IMAGE_LINK, "", text_processed)
    links = re.findall(REGEX_LINK, text_processed)
    clean_links = list(set([(el[0] + "://" + el[1] + el[2]).lower() for el in links]))
    text_processed = re.sub(REGEX_LINK, "", text_processed)
    emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text_processed)
    return clean_links, clean_links_images, emails

def remove_duplicate_unhashable(list_of_unhashable:list) -> list:
    """
    Used to keep unique Account-linked data tuples in a person object. Code isn't clean, but it gets the job done.
    """
    unique_lists = []
    unique_types = []
    for sublist in list_of_unhashable:
        type_sub = type(sublist).__name__
        if type_sub not in unique_types or sublist not in unique_lists :
            unique_lists.append(sublist)
            unique_types.append(type_sub)
    return unique_lists

def import_submodules(package = "philINT.modules"):
    """
    Get all the submodules
    Adapted from holehe's code
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if is_pkg:
            results.update(import_submodules(full_name))
    return results

def get_functions(modules):
    """
    Transform the modules objects to functions
    Adapted from holehe's code
    """
    from_email = []
    from_username = []
    for module in modules:
        if len(module.split(".")) > 3:
            if "from_email" in modules[module].__dict__:
                from_email.append(modules[module].__dict__["from_email"])
            if "from_username" in modules[module].__dict__:
                from_username.append(modules[module].__dict__["from_username"])
    return from_email, from_username

from_email, from_username = get_functions(import_submodules())

async def get_data_from_email_coro(email:str) -> list:
    """Get all the data you can gather from an email address"""
    results = []
    for m in from_email:
        result = await m(email)
        if result != None:
            results.append(result)
    return data_cleaner(results)

async def get_data_from_username_coro(username:str) -> list:
    """Get all the data you can gather from an username"""
    results = []
    for m in from_username:
        result = await m(username)
        if result != None:
            results.append(result)
    return data_cleaner(results)

def get_data_from_email(email:str) -> list:
    """
    I hate forgetting await - why not remove it ?
    Be careful - it is NOT working in jupyter notebooks !! Please use get_data_from_email_coro
    """
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_data_from_email_coro(email))
    loop.run_until_complete(task)
    return task.result()

def get_data_from_username(username:str) -> list:
    """
    I hate forgetting await - why not remove it ?
    Be careful - it is NOT working in jupyter notebooks !! Please use get_data_from_username_coro
    """
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_data_from_username_coro(username))
    loop.run_until_complete(task)
    return task.result()

def all_data_to_dict(all_data):
    """
    Makes a dictionnary from the all_data field
    """
    return {type(el).__name__:{el._fields[i]:el[i] for i in range(len(el)) if el[i] is not None} for el in all_data}

def all_data_export(all_data, file_name:str="data_export"):
    """
    Saves the all_data field to a .json file.
    Default file name is "data_export_[timestamp]"
    """
    dico = all_data_to_dict(all_data)
    json_string = json.dumps(dico, sort_keys=True, indent=4)
    timestamp = ""
    if file_name == "data_export":
        timestamp = "_" + str(round(datetime.datetime.timestamp(datetime.datetime.now())))
    with open(file_name + timestamp + ".json", "w") as f:
        f.write(json_string)

def isnamedtupleinstance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple: return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple): return False
    return all(type(n)==str for n in f)

def display_namedtuple(nt, with_title = True, tab = ""):
    """
    Displays a NamedTuple in a nice way
    """
    if with_title:
        print(tab + type(nt).__name__.replace("_", " ") + " :")
    for i in range(len(nt)):
        to_print = "\t • "
        to_print += nt._fields[i].replace("_", " ") + " : "
        if type(nt[i]) == str:
            to_print += nt[i].replace("_", " ")
            print(tab + to_print)
        elif type(nt[i]) == list:
            print(tab + to_print)
            for el in nt[i]:
                if isnamedtupleinstance(el):
                    display_namedtuple(el, with_title = False, tab= tab + "\t")
                    if el != nt[i][-1]:
                        print()
                else:
                    print("\t • " + str(el))
        elif isnamedtupleinstance(nt[i]):
            print(tab + to_print)
            display_namedtuple(nt[i], with_title = False, tab="\t")
        else:
            to_print += str(nt[i])
            print(tab + to_print)

def all_data_display(all_data):
    """
    Displays the all_data field in a nicer way
    """
    for nt in all_data:
        display_namedtuple(nt)
        print()


def print_results_banner():
    print("philINT - by Emmanuel Ajuelos (https://github.com/ajuelosemmanuel)")
    print("-------------------------------------")
    print("|              Results              |")
    print("-------------------------------------")

async def get_additionnal_info_email_eva_coro(email:str) -> tuple:
    """
    Coroutine to get information from Email Verification API (EVA - eva.pingutil.com)
    """
    async with httpx.AsyncClient() as client:
        eva_data = await client.get("http://api.eva.pingutil.com/email?email=" + email)
    if eva_data.json()["status"] == "failure":
        print("EVA couldn't get information about the email address.")
        return
    return eva_data.json()["data"]["spam"], eva_data.json()["data"]["deliverable"], eva_data.json()["data"]["disposable"]

def get_additionnal_info_email_eva(email:str) -> list:
    """
    I hate forgetting await - why not remove it ?
    Be careful - it is NOT working in jupyter notebooks !! Please use get_additionnal_info_email_eva_coro
    """
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_additionnal_info_email_eva_coro(email))
    loop.run_until_complete(task)
    return task.result()

def load_gpx_file(file_path:str) -> pandas.DataFrame:
    """
    Load a GPX file into a Pandas DataFrame
    """
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        route_info = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                route_info.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation
                })
    return pandas.DataFrame(route_info)

def display_gpx_dataframe(gpx_dataframe:pandas.DataFrame, save:bool=False):
    """
    Displays a DataFrame using OpenStreetMap
    """
    route_map = folium.Map(
    location=[gpx_dataframe["latitude"][0], gpx_dataframe["longitude"][0]],
    zoom_start=13,
    tiles='OpenStreetMap',
    )
    coordinates = [tuple(x) for x in gpx_dataframe[['latitude', 'longitude']].to_numpy()]
    folium.PolyLine(coordinates, weight=6).add_to(route_map)
    route_map.show_in_browser()
    if save:
        route_map.save(outfile = datetime.datetime.now().strftime('%Y%m%d%H%M') + ".html")