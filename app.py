from flask import Flask, request
import re

app = Flask(__name__)

PORT = 4390


@app.route('/')
def homepage():
    return "Howdy hacker!!"

@app.route('/scheduleme', methods=['POST'])
def scheduleme():
    raw_text = request.form.get('text')
    text_array = re.findall(r'"(.*?)"', raw_text)
    if len(text_array) != 3: 
        return 'The format is /scheduleme "[title]" "[start date & time]" "[end date & time]"'
    title, start, end = text_array 
    return 'Sweet I parsed the title: {}, start: {} and end: {}'.format(title, start, end)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
