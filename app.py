from flask import Flask, request
import re
import os
import requests
import dateparser

app = Flask(__name__)

PORT = 4390


@app.route('/')
def homepage():
    return "Howdy hacker!!"

@app.route('/scheduleme', methods=['POST'])
def scheduleme():
    raw_text = str(request.form.get('text'))
    text_array = re.findall(r'"(.*?)"', raw_text)
    if len(text_array) != 3: 
        return 'The format is /scheduleme "[title]" "[start date & time]" "[end date & time]"'
    title, start, end = text_array 
    
    calendar_id = os.environ.get('CALENDAR_ID')
    assert calendar_id is not None, 'Missing `CALENDAR_ID` config variable'
    access_token = os.environ.get('ACCESS_ID')
    assert access_token is not None, 'Missing `ACCESS_TOKEN` config variable'
    timezone = os.environ.get('TIMEZONE')
    assert timezone is not None, 'Missing `TIMEZONE` config variable'

    timezone_settings = {
        'TIMEZONE': timezone,
        'RETURN_AS_TIMEZONE_AWARE': True
    }
    json = {
        'calendar_id': calendar_id,
        'title': title,
        'when': {
            'start_time': int(dateparser.parse(start, settings=timezone_settings).timestamp()),
            'end_time': int(dateparser.parse(end, settings=timezone_settings).timestamp())
        }
    }
    headers = {'authorization': access_token}

    try:
        response = requests.post('https://api.nylas.com/events', headers=headers, json=json)
        if response.status_code == 200:
            return f'Wohoo! {title} was scheduled form {start} to {end}'
        else:
            return f'Error! Our reponse has a status of {response.status_code} and text {response.text}'
    except Exception as e:
        return f'An exception {e} occured creating the event'



if __name__ == '__main__':
    app.run(debug=True, port=PORT)
