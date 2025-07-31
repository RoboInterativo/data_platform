from flask import Flask, render_template, request
import os
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/users' )
def usersget():


    return 'user1', 200


@app.route('/api/users', methods=['POST'])
def users():


    return 'user add', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
