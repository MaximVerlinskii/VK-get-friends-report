# VK get friends report
Service for getting a list of VK friends with information: 
(First name, Last name, Country, City, Date of birth (in ISO format), Sex)

Friends list sorted by name

## Installing and using the service
1. Clone the repository `git clone https://github.com/MaximVerlinskii/VK-get-friends-report.git`
2. (Optional) Create a virtual environment in a convenient way for you
3. Install required dependencies from file `requirements.txt` 
   (e.g. using pip: `pip install -r requirements.txt`)
4. (Optional) Run tests, check that everything is fine `python -m unittest -v test_services.py`
5. GET VK API token:
   * Create Standalone-application at VK [click](https://vk.com/editapp?act=create)
   * On the "Settings" tab of the application, copy the application ID
   * Make a URL: 
     `https://oauth.vk.com/authorize?client_id=IDAPP&scope=friends,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.21&response_type=token`
     Here, instead of IDAPP, you need to insert the ID of your application (from the previous paragraph)
   * Go to the URL from the previous paragraph
   * It redirects to a URL like this::
     `https://oauth.vk.com/blank.html#access_token=ACCESS_TOKEN&expires_in=0&user_id=USER_ID`
     Here ACCESS_TOKEN is what we need, copy it for further use
6. The received ACCESS_TOKEN can be entered into the program manually each time, or you can write it as a string 
   to the `your_access_token` variable in the `config.py` file, 
   you can also pass the token to the `ACCESS_TOKEN` environment variable when starting the service in any way 
   convenient for you
7. Run service `python main.py`
8. Choosing a method for passing the API token to the program
9. Enter the user id (integer), whose friends we want to get information about
10. Select and enter the report file format from the possible ones or press Enter to select the `csv` format
11. Write the file name (without extension) (example: `result`) or the path and file name (without extension) 
    (example: `results/res1`) or press Enter to select the file name `report` (the `report` file is created in 
    the root directories)
12. If everything is successful, the desired file is created.
    If there are errors, information about them is displayed, information is also saved to the `file.log` file 
    (this file is re-created every time the service starts)

## What if you need to submit a report in YAML format?
In order to add a new report format (for example: `YAML`), you need to:
1. Add this format to the `available_formats` list at the top of the `services.py` file
2. Create a class by inheriting it from the abstract class `ReportFile` (for example `YamlReportFile`) 
3. Implement in the created class the logic of creating a file in the `__init__` method, which accepts one variable 
   `path_report_file: str`, which contains the file name (without format) or the path to the file and its name 
   (without format) For example: `result` or `results/res1`
4. Implement in the created class the logic of filling the file in the `add` method, which takes one variable 
   `list_of_users: list[User]`, which receives a list of objects of the User class
5. In the generated class, implement the logic for completing the filling of the file, if necessary, in the 
   `complete` method, or create this method and leave it empty
6. Add to the `create_and_prepare_file` function in the `services.py` file one more `case` in the logic branch, similar 
   to the others, in this case, you need to return the object of 
   the new class created earlier in the previous paragraphs

## What if there is not enough RAM?
The service has pagination. In the config file, in the `FRIENDS_PER_REQUEST` variable, 
you can reduce the number of entries requested in one request

## Brief scheme of the program

![Brief scheme of the program](https://sun9-east.userapi.com/sun9-32/s/v1/if2/XZgua2z2SzFFhkNUKkW08jN0l50Q391_oOH0UCtnkFQnmms0iqqsVtkYmhAAVYCtsDgUTJDWdPi4CVPqWOTnOe-H.jpg?size=611x401&quality=96&type=album "Brief scheme of the program")


## Description of the API of VK endpoints that are involved in the script

The script produces two types of `GET` requests:
1. `GET https://api.vk.com/method/friends.get?user_id=USER_ID&access_token=ACCESS_TOKEN&v=5.81`
   
   Here, a successful response looks like this:
   ```json
   {"response": 
       {
       "count": 2,
       "items": [1, 2]
       }
   }
   ```
   A bad response here looks like this:
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
     
   Here, a successful response looks like this:

   ```json
   {"response": {
       "count": 2, 
       "items": [
           {
               "id": 187844364,
               "bdate": "18.3", 
               "city": {"id": 1, "title": "City1"},
               "country": {"id": 1, "title": "Country1"}, 
               "track_code": "abcd1234", 
               "sex": 1, 
               "first_name": "First name1", 
               "last_name": "Last name1"
           },
    
           {
               "id": 215883489, 
               "bdate": "2.11.1982", 
               "city": {"id": 2, "title": "City12"}, 
               "country": {"id": 2, "title": "Country2"}, 
               "track_code": "abc123", 
               "sex": 2, 
               "first_name": "First name2", 
               "last_name": "Last name2"
           }
           ]
       }
   }
   ```

   A bad response here looks like this:
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
## Ideas for the future life of the service
* Refactoring + adding tests - `version 0.9`
* Improved error trapping and logging, adding error trapping and logging to file creation 
  (work of ReportFile descendant classes) - `version 1.0`
* Creating a docker-image, pushing it on docker-hub
* Adding the ability to write results to various databases (PostgreSQL, MongoDB), creating docker-compose for these 
  solutions - `version 1.5`
* Packing the solution into a web micro-service on FastAPI with a user-friendly interface 
  (single-page application on React) - `version 2.0`
   

