TOKEN = '5372089312:AAGU9B0PZ8kjB_Yj7hc3O-omy8UQRzWzNnw'
URL = 'https://api.telegram.org/bot{token}/{method}'

UPDATE_METH = 'getUpdates'
SEND_METH = 'sendMessage'


UPDATE_ID_FILE_PATH = 'update_id'

with open(UPDATE_ID_FILE_PATH) as file:
    data = file.readline()
    if data:
        data = int(data)
    UPDATE_ID = data

WEATHER_TOKEN = 'a57c158717de8f8244601f91987cc2b6'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?units=metric&appid={token}&q={city}'
