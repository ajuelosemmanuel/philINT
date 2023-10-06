import philINT.utils as utils

class Email:
    """
    An Email address with :
        connections     : information gathered from websites from the email address
        is_pwned        : was the email in a data leak/breach - Requires an HIBP API key that you can buy here : https://haveibeenpwned.com/API/Key
        is_spam         : is this considered as a spam email address
        is_deliverable  : can it receive an email
        is_disposable   : is it a temporary email address
    """
    def __init__(self, email_address:str):
        self.email_address = email_address
        self.connections = None
        self.is_pwned = None
        self.is_spam = None
        self.is_deliverable = None
        self.is_disposable = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def display(self):
        print("Email address : " + self.email_address)
        for field, value in self:
            if value is not None and field not in ["email_address", "connections"]:
                print("\t • " + field[3:].capitalize() + " : " + str(value))

    async def make_connections_coro(self):
        """
        Coroutine to get information from an email address from "common" websites.
        Works with jupyter notebooks.
        """
        self.connections = await utils.get_data_from_email_coro(self.email_address)

    def make_connections(self):
        """
        Function to get information from an email address from "common" websites.
        It doesn't work with jupyter notebooks.
        """
        self.connections = utils.get_data_from_email(self.email_address)
    
    async def get_additionnal_info_eva_coro(self):
        """
        Adds data from Email Verification API
        Works with jupyter notebooks.
        """
        result = await utils.get_additionnal_info_email_eva_coro(self.email_address)
        self.is_spam = result[0]
        self.is_deliverable = result[1]
        self.is_disposable = result[2]
    
    def get_additionnal_info_eva(self):
        """
        Adds data from Email Verification API
        Doesn't work with jupyter notebooks.
        """
        result = utils.get_additionnal_info_email_eva(self.email_address)
        self.is_spam = result[0]
        self.is_deliverable = result[1]
        self.is_disposable = result[2]

    async def run_all_coro(self):
        """
        Gets data from every source available on the tool for an email address
        Works with jupyter notebooks.
        """
        await self.get_additionnal_info_eva_coro()
        await self.make_connections_coro()
    
    def run_all(self):
        """
        Gets data from every source available on the tool for an email address
        Doesn't work with jupyter notebooks.
        """
        self.get_additionnal_info_eva()
        self.make_connections()

class Username:
    """
    An Username with :
        connections     : information gathered from websites from the email address
    """
    def __init__(self, username:str):
        self.username = username
        self.connections = None
    
    async def make_connections_coro(self):
        """
        Coroutine to get information from an username from "common" websites.
        Works with jupyter notebooks.
        """
        self.connections = await utils.get_data_from_username_coro(self.username)

    def make_connections(self):
        """
        Function to get information from an username from "common" websites.
        It doesn't work with jupyter notebooks.
        """
        self.connections = utils.get_data_from_username(self.username)

class Person:
    """
    A Person is supposed to be a real-life human. The object can be instantiated then "filled" with data from an email address or an username.
    It is designed to help investigators by removing redundant info, but still contains all the data for more in-depth searching.
    It stores specifically :
        email_addresses
        usernames
        names
        phone_numbers
        pictures
        accounts
        all_data
    """
    def __init__(self):
        self.email_addresses = []
        self.usernames = []
        self.names = []
        self.phone_numbers = []
        self.pictures = []
        self.accounts = []
        self.all_data = []
    
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
    
    def fill_from_email(self, email:Email):
        """
        Fills a Person object with data from an Email object
        """
        self.email_addresses = list(set(self.email_addresses + [email.email_address] + [connection.Emails for connection in email.connections if "Mails" in connection._fields and connection.Mails is not None]))
        self.usernames = list(set(self.usernames + [connection.Username for connection in email.connections if "Username" in connection._fields and connection.Username is not None]))
        self.names = list(set(self.names + [connection.Name for connection in email.connections if "Name" in connection._fields and connection.Name is not None]))
        self.phone_numbers = list(set(self.phone_numbers + [connection.Phone_number for connection in email.connections if "Phone_number" in connection._fields and connection.Phone_number is not None ]))
        self.all_data = utils.remove_duplicate_unhashable(self.all_data + email.connections)
        self.accounts = list(set(self.accounts + ["Chess.com" if type(el).__name__ == "Chess" else type(el).__name__ for el in email.connections]))
        pics = []
        for connection in email.connections:
            if "Picture" in connection._fields and connection.Picture is not None:
                pics.append(connection.Picture)
            if "Pictures" in connection._fields and connection.Pictures is not None:
                pics += connection.Pictures
        self.pictures = list(set(self.pictures + pics))

    def fill_from_username(self, username:Username):
        """
        Fills a Person object with data from an Username object
        """
        emails = self.email_addresses
        for connection in username.connections:
            if "Emails" in connection._fields:
                for email in connection.Emails:
                    if email is not None:
                        emails.append(email)
        self.email_addresses = list(set(emails))
        self.usernames = list(set(self.usernames + [username.username] + [connection.Username for connection in username.connections if "Username" in connection._fields and connection.Username is not None]))
        self.names = list(set(self.names + [connection.Name for connection in username.connections if "Name" in connection._fields and connection.Name is not None]))
        self.phone_numbers = list(set(self.phone_numbers + [connection.Phone_number for connection in username.connections if "Phone_number" in connection._fields and connection.Phone_number is not None ]))
        self.all_data = utils.remove_duplicate_unhashable(self.all_data + username.connections)
        self.accounts = list(set(self.accounts + ["Chess.com" if type(el).__name__ == "Chess" else type(el).__name__ for el in username.connections]))
        pics = []
        for connection in username.connections:
            if "Picture" in connection._fields and connection.Picture is not None:
                pics.append(connection.Picture)
            if "Pictures" in connection._fields and connection.Pictures is not None:
                pics += connection.Pictures
        self.pictures = list(set(self.pictures + pics))

    def display(self):
        """
        Displays a Person object in a prettier way
        """
        for k, v in self:
            if v != [] and k != "all_data":
                print(k.replace("_", " ").capitalize() + " :")
                for el in v:
                    if type(el) is str:
                        print("\t • " + el)
    
    def export_raw_data(self, file_name:str="data_export"):
        """
        Saves the all_data field to a .json file.
        Default file name is "data_export_[timestamp]"
        """
        utils.all_data_export(self.all_data, file_name)

    def display_raw_data(self):
        """
        Displays the all_data field in a nicer way
        """
        utils.all_data_display(self.all_data)