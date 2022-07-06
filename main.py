from sys import exit as sexit

from loguru import logger

from services import get_app_launch_info_from_user, create_and_fill_vk_friends_report


def main():

    print('Hello, welcome to VK get friends report service')
    print('-----------------------------------------------')
    try:
        access_token, user_id, format_report_file, path_report_file = get_app_launch_info_from_user()

    except Exception as Ex:
        print('''An error occurred while passing parameters to start the service
                 Make sure the entered data is correct and try again''')
        print(f'Error: {Ex}')
        logger.error(f'An error occurred while passing parameters to start the service: {Ex}')
        sexit()
    else:
        logger.info('Parameters to start the service successfully accepted')

        print('-----------------------------------------------')
        print('........Preparing report file........Please wait........')
        create_and_fill_vk_friends_report(access_token, user_id, format_report_file, path_report_file)

        logger.info(f'Report successfully created: {path_report_file}.{format_report_file}')
        print('---------------------------------------------------------------')
        print(f'Report successfully created: {path_report_file}.{format_report_file}')


if __name__ == '__main__':
    logger.add(open('file.log', 'w'), format='{time} {level} {message}')
    main()
