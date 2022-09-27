import json
import time

import requests

import const


def get_update():
    url = const.URL.format(token=const.TOKEN, method=const.UPDATE_METH)
    response = requests.get(url)
    to_dict = json.loads(response.text)
    result = to_dict.get('result')
    last_value = result[-1]
    return last_value


def get_update_id(last_value):
    update_id = last_value.get('update_id')
    return update_id


def save_update_id(update):
    with open(const.UPDATE_ID_FILE_PATH, 'w') as f:
        f.write(str(update['update_id']))
    const.UPDATE_ID = update['update_id']
    return True


def get_user_id(last_value):
    try:
        user_id = last_value.get('message').get('chat').get('id')
    except AttributeError:
        user_id = last_value.get('my_chat_member').get('chat').get('id')
    return user_id


def get_user_name(last_value):
    try:
        user_name = last_value.get('message').get('chat').get('first_name')
    except AttributeError:
        user_name = last_value.get('my_chat_member').get('chat').get('first_name')
    return user_name


def get_message(last_value):
    try:
        message = last_value.get('message').get('text')
        if message == '/start':
            send_message(f'Hello {get_user_name(get_update())}!')
            send_message('What city do you want to know the weather?')
        else:
            return message
    except AttributeError:
        send_message(f'Hello {get_user_name(get_update())}!')
        send_message('What city do you want to know the weather?')
        return


def send_message(message):
    url = const.URL.format(token=const.TOKEN, method=const.SEND_METH)
    data = {
        'chat_id': get_user_id(get_update()),
        'text': message
    }
    response = requests.post(url, data).text
    return response


def get_weather_data(city_name):
    url = const.WEATHER_URL.format(token=const.WEATHER_TOKEN, city=city_name)
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    data = json.loads(response.content)
    result = data.get('main').get('temp')
    if city_name is None:
        pass
    else:
        msg = f'Temperature in {city_name} is {result} °С'
        return msg


def main():

    while True:
        update = get_update()

        if const.UPDATE_ID != get_update_id(update):

            result = get_weather_data(get_message(update))
            send_message(result)
            save_update_id(update)

        time.sleep(1)


if __name__ == '__main__':
    main()

