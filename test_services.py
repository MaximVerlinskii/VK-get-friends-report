import os
import unittest
from services import VkResponseData, User, JsonReportFile, CsvReportFile, TsvReportFile


# NEED MORE TESTS !!!!
# TODO create more tests (increase code coverage with tests)


class TestVkResponseData(unittest.TestCase):
    def test_make_bd_iso_format_str(self):
        self.assertEqual(VkResponseData._make_bd_iso_format_str(None), None)
        self.assertEqual(VkResponseData._make_bd_iso_format_str('1.2.2000'), '2000-02-01')
        self.assertEqual(VkResponseData._make_bd_iso_format_str('1.3'), '03-01')
        self.assertEqual(VkResponseData._make_bd_iso_format_str('05.01.1999'), '1999-01-05')
        self.assertEqual(VkResponseData._make_bd_iso_format_str('15.1.1998'), '1998-01-15')
        self.assertEqual(VkResponseData._make_bd_iso_format_str('21.12.1997'), '1997-12-21')
        self.assertEqual(VkResponseData._make_bd_iso_format_str('5.10.2000'), '2000-10-05')
        self.assertEqual(VkResponseData._make_bd_iso_format_str('29.2'), '02-29')

    def test_make_sex_str(self):
        self.assertEqual(VkResponseData._make_sex_str(1), 'Female')
        self.assertEqual(VkResponseData._make_sex_str(2), 'Male')

    def test_make_country_str_or_none(self):
        self.assertEqual(VkResponseData._make_country_str_or_none(None), None)
        vk_country_1 = {'id': 4, 'title': 'Казахстан'}
        self.assertEqual(VkResponseData._make_country_str_or_none(vk_country_1), 'Казахстан')
        vk_country_2 = {'id': 1, 'title': 'Россия'}
        self.assertEqual(VkResponseData._make_country_str_or_none(vk_country_2), 'Россия')
        vk_country_3 = {'id': 129, 'title': 'Монако'}
        self.assertEqual(VkResponseData._make_country_str_or_none(vk_country_3), 'Монако')

    def test_make_city_str_or_none(self):
        self.assertEqual(VkResponseData._make_country_str_or_none(None), None)
        vk_city_1 = {'id': 151, 'title': 'Уфа'}
        self.assertEqual(VkResponseData._make_country_str_or_none(vk_city_1), 'Уфа')
        vk_city_2 = {'id': 99, 'title': 'Новосибирск'}
        self.assertEqual(VkResponseData._make_country_str_or_none(vk_city_2), 'Новосибирск')
        vk_city_3 = {'id': 110, 'title': 'Пермь'}
        self.assertEqual(VkResponseData._make_country_str_or_none(vk_city_3), 'Пермь')

    def test_list_of_users(self):
        # test_vk_data is not real vk response data

        test_vk_data = {'response':
                            {'count': 5000, 'items':
                                [{'id': 518784344364,
                                  'bdate': '17.4',
                                  'city': {'id': 49, 'title': 'Екатеринбург'},
                                  'country': {'id': 1, 'title': 'Россия'},
                                  'track_code': '6bb2ed2c4jguNZX_5N8a3NwkkkEQ',
                                  'sex': 1,
                                  'first_name': 'Ирина',
                                  'last_name': 'Γригорьева'},
                                 {'id': 52158834389,
                                  'bdate': '20.3.1971',
                                  'city': {'id': 1, 'title': 'Москва'},
                                  'country': {'id': 1, 'title': 'Россия'},
                                  'track_code': 'b8938a0fzhCy_Ixt4jZOKmFXcU',
                                  'sex': 2,
                                  'first_name': 'Αндрей',
                                  'last_name': 'Εвсекеев'},
                                 {'id': 62696323428,
                                  'city': {'id': 1, 'title': 'Москва'},
                                  'country': {'id': 1, 'title': 'Россия'},
                                  'track_code': '3a28c6b4OI0Fel4xbwQHsG',
                                  'sex': 2,
                                  'first_name': 'Денис',
                                  'last_name': 'Креев'},
                                 {'id': 6217630097,
                                  'city': {'id': 95, 'title': 'Нижний Новгород'},
                                  'country': {'id': 1, 'title': 'Россия'},
                                  'track_code': 'e91dee05uD65-rHC6mCrH8',
                                  'sex': 2,
                                  'first_name': 'Никита',
                                  'last_name': 'Ηикитин'},
                                 {'id': 62376887833,
                                  'bdate': '4.7.1983',
                                  'city': {'id': 1, 'title': 'Москва'},
                                  'country': {'id': 1, 'title': 'Россия'},
                                  'track_code': '791ab652prf4Uvps_fG',
                                  'sex': 1,
                                  'first_name': 'Βячеслава', 'last_name': 'Невзорова'}
                                 ]
                             }
                        }
        vk_resp_data = VkResponseData(test_vk_data)
        user1 = User(first_name='Ирина', last_name='Γригорьева', country='Россия', city='Екатеринбург',
                     birth_date='04-17', sex='Female')
        user2 = User(first_name='Αндрей', last_name='Εвсекеев', country='Россия', city='Москва',
                     birth_date='1971-03-20', sex='Male')
        user3 = User(first_name='Денис', last_name='Креев', country='Россия', city='Москва',
                     birth_date=None, sex='Male')
        user4 = User(first_name='Никита', last_name='Ηикитин', country='Россия', city='Нижний Новгород',
                     birth_date=None, sex='Male')
        user5 = User(first_name='Βячеслава', last_name='Невзорова', country='Россия', city='Москва',
                     birth_date='1983-07-04', sex='Female')
        users_list = [user1, user2, user3, user4, user5]

        self.assertEqual(vk_resp_data.list_of_users, users_list)


class TestJsonReportFile(unittest.TestCase):
    def test_creation_file(self):
        JsonReportFile('temp_for_test')
        with open('temp_for_test.json', 'r', encoding='UTF-8') as r_f:
            file_content = r_f.readline()
        os.remove('temp_for_test.json')
        self.assertEqual(file_content, '[')

    def test_filling_file(self):
        rep_file = JsonReportFile('temp_for_test')
        my_user = User(first_name='Ирина', last_name='Γригорьева', country='Россия', city='Екатеринбург',
                       birth_date='04-17', sex='Female')
        rep_file.add([my_user])
        rep_file.complete()
        with open('temp_for_test.json', 'r', encoding='UTF-8') as r_f:
            file_content = r_f.readlines()[0]
        os.remove('temp_for_test.json')
        expected_file_content = '[{"first_name": "Ирина", "last_name": "Γригорьева", "country": "Россия",' \
                                ' "city": "Екатеринбург", "birth_date": "04-17", "sex": "Female"},\n'
        self.assertEqual(file_content, expected_file_content)


class TestCsvReportFile(unittest.TestCase):
    def test_creation_file(self):
        CsvReportFile('temp_for_test')
        with open('temp_for_test.csv', 'r', encoding='UTF-8') as r_f:
            file_content = r_f.readline()
        os.remove('temp_for_test.csv')
        self.assertEqual(file_content, 'first_name,last_name,country,city,birth_date,sex\n')

    def test_filling_file(self):
        rep_file = CsvReportFile('temp_for_test')
        my_user = User(first_name='Ирина', last_name='Γригорьева', country='Россия', city='Екатеринбург',
                       birth_date='04-17', sex='Female')
        rep_file.add([my_user])
        rep_file.complete()
        with open('temp_for_test.csv', 'r', encoding='UTF-8') as r_f:
            file_content = r_f.readlines()
        os.remove('temp_for_test.csv')
        expected_file_content = ['first_name,last_name,country,city,birth_date,sex\n',
                                 'Ирина,Γригорьева,Россия,Екатеринбург,04-17,Female\n']
        self.assertEqual(file_content, expected_file_content)


class TestTsvReportFile(unittest.TestCase):
    def test_creation_file(self):
        TsvReportFile('temp_for_test')
        with open('temp_for_test.tsv', 'r', encoding='UTF-8') as r_f:
            file_content = r_f.readline()
        os.remove('temp_for_test.tsv')
        self.assertEqual(file_content, 'first_name\tlast_name\tcountry\tcity\tbirth_date\tsex\n')

    def test_filling_file(self):
        rep_file = TsvReportFile('temp_for_test')
        my_user = User(first_name='Ирина', last_name='Γригорьева', country='Россия', city='Екатеринбург',
                       birth_date='04-17', sex='Female')
        rep_file.add([my_user])
        rep_file.complete()
        with open('temp_for_test.tsv', 'r', encoding='UTF-8') as r_f:
            file_content = r_f.readlines()
        os.remove('temp_for_test.tsv')
        expected_file_content = ['first_name\tlast_name\tcountry\tcity\tbirth_date\tsex\n',
                                 'Ирина\tΓригорьева\tРоссия\tЕкатеринбург\t04-17\tFemale\n']
        self.assertEqual(file_content, expected_file_content)


class TestUser(unittest.TestCase):
    def test_user_to_dict(self):
        test_user = User(first_name='Ирина', last_name='Γригорьева', country='Россия', city='Екатеринбург',
                       birth_date='04-17', sex='Female')
        test_user_dict = test_user.get_dict()
        expected_dict = {"first_name": "Ирина", "last_name": "Γригорьева", "country": "Россия",
                         "city": "Екатеринбург", "birth_date": "04-17", "sex": "Female"}
        self.assertEqual(test_user_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
