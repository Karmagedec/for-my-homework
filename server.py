import time
from datetime import datetime
from flask import Flask, request


app = Flask(__name__)
messages = [
    {'username': 'John', 'time': time.time(), 'text': 'Hello!'},
    {'username': 'Mary', 'time': time.time(), 'text': 'Hello, John!'},
]
password_storage = {
    'John': '12345',
    'Mary': '54321'
}





@app.route("/")
def hello_method():
    return "Hello, World! 123"



@app.route("/status")
def status_method():
    return {
        'status': True,
        'datetime': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'messages': 'Total messages:'+str(len(messages)),
        'users':" Total users:"+str(len(password_storage))
    }


@app.route("/send", methods=['POST'])
def send_method():
    """
    JSON {"username": str, "password": str, "text": str}
    username, text - непустые строки
    :return: {'ok': bool}
    """
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    # first attempt for password is always valid
    if username not in password_storage:
        password_storage[username] = password


    # validate data
    if not isinstance(username, str) or len(username) == 0:
        return {'ok': False}
    if not isinstance(text, str) or len(text) == 0:
        return {'ok': False}
    if password_storage[username] != password:
        return {'ok': False}

    if startswith(upper(text),'/frown'):
        temp=text[6:]
        text=username+' неодобрительно качает головой, в знак недовольства высказываниями '+temp


    messages.append({'username': username, 'time': time.time(), 'text': text})

    return {'ok': True}


@app.route("/messages")
def messages_method():
    """
    Param after - отметка времени после которой будут сообщения в результате
    :return: {'messages': [
        {'username': str, 'time': float, 'text': str},
        ...
    ]}
    """
    after = float(request.args['after'])
    filtered_messages = [message for message in messages if message['time'] > after]
    return {'messages': filtered_messages}


app.run()
