import json
import os
import csv
from sys import exit as sexit
from time import sleep
from typing import NamedTuple, Literal
from datetime import datetime
from abc import abstractmethod, ABC

import requests
from loguru import logger

from config import ACCESS_TOKEN, FRIENDS_PER_REQUEST

available_formats = ('csv', 'tsv', 'json')

# USER


class User(NamedTuple):
    """
    Used to store user(friend) data
    """
    @staticmethod
    def user_fields() -> tuple:
        return 'first_name', 'last_name', 'country', 'city', 'birth_date', 'sex'

    def __eq__(self, other):        # Needed for tests
        if isinstance(other, User):
            is_equals_first_name = self.first_name == other.first_name
            is_equals_last_name = self.last_name == other.last_name
            is_equals_country = self.country == other.country
            is_equals_city = self.city == other.city
            is_equals_birth_date = self.birth_date == other.birth_date
            is_equals_sex = self.sex == other.sex
            return all((is_equals_first_name, is_equals_last_name, is_equals_country, is_equals_city,
                        is_equals_birth_date, is_equals_sex))

        return False

    def get_dict(self) -> dict:
        """
        Convert User to dict object
        :return: user_dict (dict)
        """

        user_dict = {'first_name': self.first_name,
                     'last_name': self.last_name,
                     'country': self.country,
                     'city': self.city,
                     'birth_date': self.birth_date,
                     'sex': self.sex}
        return user_dict

    first_name: str
    last_name: str
    country: str | None
    city: str | None
    birth_date: str | None
    sex: str | None


# Report files

class ReportFile(ABC):
    """
    An abstract class for writing report in different formats
    To create a new format, you must inherit from this class and implement three methods: __init__ , add, complete
    """

    @abstractmethod
    def __init__(self, path_report_file: str):
        """
        Creates and prepares a file for writing data
        :param path_report_file: (str)
        """
        pass

    @abstractmethod
    def add(self, list_of_users: list[User]):
        """
        Appends data to an existing file
        :param list_of_users: (list[User])
        """
        pass

    @abstractmethod
    def complete(self):
        """
        Refine the file if necessary
        :return:
        """
        pass


class CsvReportFile(ReportFile):
    """
    Class for writing report in csv file report
    """

    def __init__(self, path_report_file: str):
        """
        Creates a csv file in path_report_file and writes table header
        For example: if path_report_file = 'results/res1', 'results/res1.csv' will be created
        :param path_report_file: (str)
        """
        self.path_report_file = path_report_file     # Saves the path to an instance of the class
        with open(f'{path_report_file}.csv', 'w', encoding='UTF-8', newline='') as csv_file:  # Creating csv file and
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(User.user_fields())                                               # write table header

    def add(self, list_of_users: list[User]):
        """
        Adds user records to a csv file
        :param list_of_users: (list[User])
        """
        with open(f'{self.path_report_file}.csv', 'a', encoding='UTF-8', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(list_of_users)

    def complete(self):
        """
        This is not necessary for csv files
        """
        pass


class TsvReportFile(ReportFile):
    """
    Class for writing report in tsv file report
    """

    def __init__(self, path_report_file: str):
        """
        Creates a tsv file in path_report_file and writes table header
        For example: if path_report_file = 'results/res1', 'results/res1.tsv' will be created
        :param path_report_file: (str)
        """
        self.path_report_file = path_report_file      # Saves the path to an instance of the class
        with open(f'{path_report_file}.tsv', 'w', encoding='UTF-8', newline='') as tsv_file:   # Creating tsv file and
            writer = csv.writer(tsv_file, delimiter='\t')
            writer.writerow(User.user_fields())                                                # write table header

    def add(self, list_of_users: list[User]):
        """
        Adds user records to a tsv file
        :param list_of_users: (list[User])
        """
        with open(f'{self.path_report_file}.tsv', 'a', encoding='UTF-8', newline='') as tsv_file:
            writer = csv.writer(tsv_file, delimiter='\t')
            writer.writerows(list_of_users)

    def complete(self):
        """
        This is not necessary for tsv files
        """
        pass


class JsonReportFile(ReportFile):
    """
    Class for writing report in json file report
    """

    def __init__(self, path_report_file: str):
        """
        Creates a json file in path_report_file and writes '[' to start creation json_list
        For example: if path_report_file = 'results/res1', 'results/res1.json' will be created
        :param path_report_file: (str)
        """
        self.path_report_file = path_report_file    # Saves the path to an instance of the class
        with open(f'{path_report_file}.json', 'w', encoding='UTF-8', newline='\n') as json_file:
            json_file.write('[')

    def add(self, list_of_users: list[User]):
        """
        Adds user records to a json file
        :param list_of_users: (list[User])
        """
        with open(f'{self.path_report_file}.json', 'a', encoding='UTF-8', newline='\n') as json_file:
            for user in list_of_users:
                user_json = json.dumps(user.get_dict(), ensure_ascii=False)
                json_file.write(user_json+',\n')

    def complete(self):
        """
        Writes to file ']' to finish json_list
        """
        with open(f'{self.path_report_file}.json', 'a', encoding='UTF-8', newline='\n') as json_file:
            json_file.write(']')


# Functions

def get_access_token() -> str:
    """
    The function is needed to receive the access_token (vk access token) from the command line or
    from the virtual environment
    :return: (str) access_token
    """
    while True:
        print('Do you want get ACCESS_TOKEN from environment or enter manually?')
        print('Type "E" - from environment, \n'
              'Type "M" - enter access token manually \n'
              'Type "F" - from file "config.py"')
        way_to_get_access_token = input('')
        if way_to_get_access_token not in ('E', 'M', 'F'):
            print('Incorrect input, try again')
            continue
        else:
            break
    access_token: str = ''
    match way_to_get_access_token:
        case "E":
            access_token: str = os.environ.get('ACCESS_TOKEN')
        case "M":
            access_token: str = input('Enter vk access_token: ')
        case "F":
            access_token: str = ACCESS_TOKEN
            # exec(open('config.py').read())
            # access_token: str = os.environ.get('ACCESS_TOKEN')

    return access_token


def get_format_of_report_file() -> str:
    """
    The function is needed to get the format of the report file from the command line
    Available formats specified in a global variable "available_formats" in this file
    :return: (str) format_report_file
    """
    while True:
        format_report_file_temp = input(f'Choose format of report file (available formats: {available_formats})'
                                        f' or press "Enter" to choose the csv: ')
        if format_report_file_temp == '':
            return 'csv'

        elif format_report_file_temp not in available_formats:
            print('Incorrect format of report file, try again')
            format_report_file = 'csv'
            continue
        else:
            return format_report_file_temp

    return format_report_file


def get_path_of_report_file(format_report_file):
    """
    The function is needed to get the path and file name of the report from the command line
    :param format_report_file: (str) on of available_formats (global variable)
    :return: (str) path_report_file_temp
    """
    while True:
        path_report_file_temp = input(f'Enter path to report file (example: type "results/resfile" to create '
                                      f'"results/resfile.{format_report_file}") or press "Enter" to create '
                                      f'file "report.{format_report_file}" in current directory: ')

        if path_report_file_temp == '':
            return 'report'

        elif path_report_file_temp[0] == '/':
            print('Wrong path. Try again')
            continue
        else:
            return path_report_file_temp


def get_app_launch_info_from_user():
    """
    The function runs other functions (get_access_token, get_format_of_report_file, get_path_of_report_file) to get
    access_token, format_report_file, path_report_file
    The functions get the user_id from the command line
    :return: (tuple) (access_token, vk_user_id, format_report_file, path_report_file)
    """
    access_token = get_access_token()
    print('---------------------------------------------------------------')
    vk_user_id: str = input('Enter the user VK ID for which the report is required: ')
    print('---------------------------------------------------------------')
    format_report_file = get_format_of_report_file()
    print('---------------------------------------------------------------')
    path_report_file = get_path_of_report_file(format_report_file)

    if '/' in path_report_file:   # If the path is in another folder, then need to create it
        directory_with_file = '/'.join(path_report_file.split('/')[:-1])
        try:
            os.makedirs(directory_with_file)
            logger.info(f'Successful creating directory {directory_with_file}')
        except Exception as Ex:
            logger.info(f'Directory already exist ({Ex})')

    return access_token, vk_user_id, format_report_file, path_report_file


def create_and_fill_vk_friends_report(access_token, vk_user_id, format_report_file, path_of_report_file):
    """
    A function that implements the main functionality of the application
    It 1) create report file
       2) create vk friends parser
       3) get from vk api number of friends for the user_id
       4) Takes data about friends in chunks (number friends at one chunk is in the variable "friends_per_request")
       5) Immediately writes these chunks to a file
       6) Finish report file if necessary
    :param access_token: (str)
    :param vk_user_id: (str)
    :param format_report_file: (str)
    :param path_of_report_file: (str)
    """
    report_file = create_and_prepare_file(format_report_file, path_of_report_file)
    parser = VkFriendsParser(access_token, vk_user_id)
    number_of_friends = parser.get_number_of_friends()
    friends_per_request = FRIENDS_PER_REQUEST   # number friends at one "chunk"
    number_of_requests = number_of_friends//friends_per_request + 1
    for chunk_number in range(number_of_requests):
        resp_data: dict = parser.get_info_about_friends(offset=chunk_number*friends_per_request,
                                                        count=friends_per_request)
        try:
            vk_resp_data = VkResponseData(resp_data)   # get information about friends
            list_of_friends = vk_resp_data.list_of_users
        except Exception as Ex:
            print(f'An error occurred while parsing vk response data: {Ex}')
            logger.error(f'An error occurred while parsing vk response data: {Ex}')
            sexit()
        else:
            report_file.add(list_of_friends)          # save information about friends to file
    report_file.complete()


def create_and_prepare_file(format_file: str, path_file: str) -> CsvReportFile | TsvReportFile | JsonReportFile:
    """
    Function for creating an object for working with a report file, depending on the selected report file's format
    :param format_file: (str)
    :param path_file: (str)
    :return: (CsvReportFile | TsvReportFile | JsonReportFile) an object for creating file and writing information to it
                           (child of ReportFile)
    """
    match format_file:
        case 'csv':
            return CsvReportFile(path_file)
        case 'tsv':
            return TsvReportFile(path_file)
        case 'json':
            return JsonReportFile(path_file)


# Classes


class VkResponseData:
    """
    Class for working with data returned by VK API
    The main goal is to create a list of objects of class User
    """
    def __init__(self, vk_data: dict):
        """
        Create a list of objects of class User, uses protected static methods for this
        :param vk_data: (dict) request.json() from vk friends get api
        """
        self.list_of_users: list[User] = []
        for friend in vk_data['response']['items']:
            if friend.get('deactivated'):
                continue
            user = User(first_name=friend.get('first_name'),
                        last_name=friend.get('last_name'),
                        country=self._make_country_str_or_none(friend.get('country')),
                        city=self._make_city_str_or_none(friend.get('city')),
                        birth_date=self._make_bd_iso_format_str(friend.get('bdate')),
                        sex=self._make_sex_str(friend['sex'])
                        )
            self.list_of_users.append(user)

    @staticmethod
    def _make_sex_str(vk_sex: Literal[1, 2]) -> Literal['Female', 'Male']:
        """
        Converts vk sex format (1 or 2) to string sex format ('Female' or 'Male')
        :param vk_sex: (Literal[1,2]) 1 for Female or 2 for Male
        :return: (Literal['Female', 'Male']) sex of user
        """
        match vk_sex:
            case 1:
                return 'Female'
            case 2:
                return 'Male'

    @staticmethod
    def _make_country_str_or_none(vk_country: dict | None) -> str | None:  # Two identical methods
        """
        Converts vk country format (for example {'id': 1, 'title': 'Россия'}) to string country format ('Россия')
        If param vk_country is None, returns None
        :param vk_country: (dict | None)
        :return: (str | None)
        """
        if vk_country:
            return vk_country.get('title')
        return vk_country

    @staticmethod
    def _make_city_str_or_none(vk_city: dict | None) -> str | None:       # Two identical methods
        """
        Converts vk city format (for example {'id': 151, 'title': 'Уфа'}) to string country format ('Уфа')
        If param vk_city is None, returns None
        :param vk_city: (dict | None)
        :return: (str | None)
        """
        if vk_city:
            return vk_city.get('title')
        return vk_city

    @staticmethod
    def _make_bd_iso_format_str(vk_bd: str | None) -> str | None:
        """
        Converts vk birth date format (for example: 2.3.1998 or 1.5)
        to string birth date iso format ('1998-03-02' or '05-01')

        If param vk_bd is None, returns None
        :param vk_bd: (str | None)
        :return: (str | None)
        """
        if not vk_bd:
            return vk_bd
        if len(vk_bd.split('.')) == 3:
            bd_date = datetime.strptime(vk_bd, '%d.%m.%Y')
            return bd_date.isoformat()[:10]                              # crutch
        elif len(vk_bd.split('.')) == 2:
            bd_date = datetime.strptime(vk_bd+'-2016', '%d.%m-%Y')       # Some users have no year
            return bd_date.isoformat()[5:10]                             # crutch
        return None


class VkFriendsParser:
    """
    Class for requesting information from VK API friends
    """
    def __init__(self, access_token: str, vk_user_id: str):
        """
        Creates an object for working with VK API friends
        :param access_token: (str)
        :param vk_user_id: (str)
        """
        self.__access_token = access_token
        self._vk_user_id = vk_user_id

    def get_number_of_friends(self) -> int:
        """
        Function makes a web request to VK API friends
        Function to get the number of friends of user (with user_id)
        :return: (int) number of friends of user (with user_id)
        """
        params = {'user_id': self._vk_user_id,
                  'access_token': self.__access_token,
                  'v': '5.81'}
        vk_response = requests.get(url='https://api.vk.com/method/friends.get', params=params)
        sleep(1)
        try:
            result = int(vk_response.json()['response']['count'])
        except Exception as Ex:
            print('''An error occurred while getting the number of friends.
                  Possibly incorrect access_token/user_id entered or access closed.''')
            logger.error(f'An error occurred while getting the number of friends. '
                         f'Possibly incorrect access_token/user_id entered or access closed. : \n Error: {Ex}')
            if vk_response:
                print(f'Vk error: {vk_response.json()["error"]["error_msg"]}')
                logger.error(f'Vk error: {vk_response.json()["error"]["error_msg"]}')
            sexit()
        else:
            logger.info('Number of friends received successfully')
            return result

    def get_info_about_friends(self, offset: int, count: int) -> dict:
        """
        Function makes a web request to VK API
        Function to get the information about friends of user (with user_if)
        :param offset: (int) query shift for pagination
        :param count: (count)
        :return: (dict) raw vk response data (request.json())
        """
        params = {'user_id': self._vk_user_id,
                  'order': 'name',
                  'fields': 'sex, bdate, city, country',
                  'offset': offset,
                  'count': count,
                  'access_token': self.__access_token,
                  'v': '5.81'}
        vk_response = requests.get(url='https://api.vk.com/method/friends.get', params=params)
        sleep(1)

        try:
            result = vk_response.json()
        except Exception as Ex:
            print('An error occurred while getting friends list with information. '
                  'Possibly incorrect access_token/user_id entered or access closed.')
            logger.error(f'An error occurred while getting friends list with information. '
                         f'Possibly incorrect access_token/user_id entered or access closed. : \n Error {Ex}')
            if vk_response:
                print(f'VK error: {vk_response.json()["error"]["error_msg"]}')
                logger.error(f'VK error: {vk_response.json()["error"]["error_msg"]}')
            sexit()
        else:
            logger.info('Friends list with information received successfully')
            return result
