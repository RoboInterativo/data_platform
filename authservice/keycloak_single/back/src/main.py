from flask import Flask, render_template, request
import os
import requests

DB=[]
TOKEN = "7625519685:AAEbvfP93LGiUAXd8PdCCJA_tBwfHWARYlY"
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setWebhook')
def echo_set():
    data = {}
    data["url"] = "robosergflasktest.robointerativo.org/webhook"
    method = "setWebhook"
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    r = requests.post(url, json = data)
    return r.json()

def send_message(chat_id, text):
    """Отправка сообщения через API Telegram"""
    url = BASE_URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)
    DB.append(data)

    # Обработка входящего сообщения
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_text = data['message'].get('text', '')

        # Ответ на команду /start
        if message_text == '/start':
            send_message(chat_id, 'Привет! Я простой бот.')
        elif message_text == '/help':
            send_message(chat_id, 'Привет! сделать бота чатgpt.')
        else:
            # Эхо-ответ
            send_message(chat_id, f'Вы написали: {message_text}')

    return 'ok', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
