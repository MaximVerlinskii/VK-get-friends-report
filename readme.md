# VK get friends report
The English version of the documentation is in file `readme_eng.md`

Сервис для получения списка друзей ВК с информацией: (Имя, Фамилия, Страна, Город, Дата рождения (в ISO формате), Пол)

Список друзей отсортирован по именам

## Установка и использования сервиса
1. Клонировать репозиторий `git clone https://github.com/MaximVerlinskii/VK-get-friends-report.git`
2. (Опционально) Создать виртуальное окружение удобным вам способом
3. Установить необходимые зависимости из файла `requirements.txt` 
   (например с помощью pip: `pip install -r requirements.txt`)
4. (Опционально) Запустить тесты, проверить, что все хорошо `python -m unittest -v test_services.py`
5. Получить VK API token:
   * Cоздать Standalone-приложение в VK [click](https://vk.com/editapp?act=create)
   * На вкладке "Настройки" приложения копируем ID приложения
   * Формируем URL: 
     `https://oauth.vk.com/authorize?client_id=IDПРИЛОЖЕНИЯ&scope=friends,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.21&response_type=token`
     Здесь вместо IDПРИЛОЖЕНИЯ необходимо вставить ID своего приложение (из предыдущего пункта)
   * Переходим по URL из предыдущего пункта
   * Происходит перенаправление на подобный URL:
     `https://oauth.vk.com/blank.html#access_token=ACCESS_TOKEN&expires_in=0&user_id=USER_ID`
     Здесь ACCESS_TOKEN - то, что нам необходимо, копируем его для дальнейшего использования
6. Полученный ACCESS_TOKEN можно каждый раз вводить в программу вручную, а можно прописать в виде строки 
    в переменную `your_access_token` в файле `config.py`, также можно передать токен в переменную окружения 
    `ACCESS_TOKEN` при запуске сервиса любым удобным вам способом
7. Запускаем сервис `python main.py`
8. Выбираем способ передаче программе API токена
9. Вводим id пользователя (число), информацию о друзьях которого хотим получить
10. Выбираем и вводим формат файла отчета из возможных или нажимаем Enter для выбора формата `csv`
11. Пишем имя файла (без расширения) (пример: `result`) или путь и имя файла (без расширения) 
    (пример: `results/res1`) или нажимаем Enter для выбора имени файла `report` (файл `report` создается в корневой директории)
12. Если все успешно, создается нужный файл. 
    Если есть ошибки, выводится информация о них, также информация сохраняется в файл `file.log` (данный файл пересоздается каждый запуск сервиса)

## Что если потребуется отчет отдать в формате YAML?
Для того, чтобы добавить новый формат отчета (например: `YAML`), необходимо:
1. Добавить этот формат в список `available_formats` в  верхней части файла `services.py`
2. Создать класс, отнаследовав его от абстрактного класса `ReportFile` (например `YamlReportFile`) 
3. Реализовать в созданном классе логику создания файла в методе `__init__`, который принимает
   одну переменную `path_report_file: str`, в которую приходит имя файла (без формата) или путь к файлу и его имя (без формата)
   Например: `result` или `results/res1`
4. Реализовать в созданном классе логику заполнения файла в методе `add`, который принимает
   одну переменную `list_of_users: list[User]`, в которую приходит список объектов класса User
5. Реализовать в созданном классе логику завершения заполнения файла, если это необходимо, в методе
   `complete` или создайте этот метод и оставьте его пустым
6. Добавить в функцию `create_and_prepare_file` в файле `services.py` еще один `case` в ветвлении логики по аналогии с 
   остальными, в этом кейсе надо вернуть объект нового созданного ранее в предыдущих пунктах класса

## Что если не хватает оперативной памяти?
В сервисе реализована пагинация. В файле конфиг в переменной `FRIENDS_PER_REQUEST` можно уменьшить количество записей,
запрашиваемых при одном запросе

## Краткая схема работы программы

![Краткая схема работы программы](https://sun9-east.userapi.com/sun9-32/s/v1/if2/XZgua2z2SzFFhkNUKkW08jN0l50Q391_oOH0UCtnkFQnmms0iqqsVtkYmhAAVYCtsDgUTJDWdPi4CVPqWOTnOe-H.jpg?size=611x401&quality=96&type=album "Краткая схема работы программы")


## Описание API энд-поинтов VK, которые задействованы в скрипте

В скрипте производится два вида `GET` запроса:
1. `GET https://api.vk.com/method/friends.get?user_id=USER_ID&access_token=ACCESS_TOKEN&v=5.81`
   
   Здесь успешный ответ имеет следующий вид:
   ```json
   {"response": 
       {
       "count": 2,
       "items": [1, 2]
       }
   }
   ```
   Неуспешный ответ здесь имеет следующий вид:
   ```json
   {"error": {
       "error_code": 1,
       "error_msg": "Imformation about error",
       "request_params": [
           {
               "key": "user_id", 
               "value": "123"
           },   
           {
               "key": "v", 
               "value": "5.81"
           },    
           {
               "key": "method", 
               "value": "friends.get"
           },    
           {
               "key": "oauth", 
               "value": "1"
           }
           ]
       }
   }

   ```
   
2. `GET https://api.vk.com/method/friends.get?user_id=USER_ID&access_token=ACCESS_TOKEN&v=5.81&order=name&offset=OFFSET&count=COUNT&fields=sex,bdate,city,country`
     
   Здесь успешный ответ имеет следующий вид:

   ```json
   {"response": {
       "count": 2, 
       "items": [
           {
               "id": 187844364,
               "bdate": "18.3", 
               "city": {"id": 1, "title": "Город1"},
               "country": {"id": 1, "title": "Страна1"}, 
               "track_code": "abcd1234", 
               "sex": 1, 
               "first_name": "Имя1", 
               "last_name": "Фамилия1"
           },
    
           {
               "id": 215883489, 
               "bdate": "2.11.1982", 
               "city": {"id": 2, "title": "Город2"}, 
               "country": {"id": 2, "title": "Страна2"}, 
               "track_code": "abc123", 
               "sex": 2, 
               "first_name": "Имя2", 
               "last_name": "Фамилия2"
           }
           ]
       }
   }
   ```

   Неуспешный ответ здесь имеет следующий вид:
   ```json
   {"error": {
       "error_code": 1,
       "error_msg": "Information about error",
       "request_params": [
           {
           "key": "user_id", 
           "value": "123"
           },    
           {
           "key": "order",
           "value": "name"
           },   
           {
           "key": "fields", 
           "value": "sex, bdate, city, country"
           },    
           {
           "key": "offset", 
           "value": "0"
           },    
           {
           "key": "count", 
           "value": "2"
           },    
           {
           "key": "v", 
           "value": "5.81"
           },    
           {
           "key": "method", 
           "value": "friends.get"
           },    
           {
           "key": "oauth", 
           "value": "1"
           }
           ]
       }
   }

   ```
## Идеи для дальнейшей жизни сервиса
* Рефакторинг + добавление тестов - `version 0.9`
* Улучшение отлавливания и логирования ошибок, добавление отлавливания ошибок и логирование к созданию файлов (работа
классов-наследников ReportFile) - `version 1.0`
* Создание docker-image, размещение его на docker-hub
* Добавление возможности писать результаты в различные БД (PostgreSQL, MongoDB), создание docker-compose для этих 
решений - `version 1.5`
* Упаковка решения в веб микро-сервис на FastAPI с user friendly интерфейсом 
(одностраничное приложение на React) - `version 2.0`
   

