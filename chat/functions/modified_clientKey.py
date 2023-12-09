# client.py
# By Gargi Chaurasia 2019059
import socket
import sys
import pickle
from util.HashAlgo import HashAlgo
from util.Operations import Operations
from util.RSA import RSA
from util.SAES import SAES


from flask import Flask, request
app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    # Here we would add the existing encryption and sending logic
    # For now, just printing the message
    print("Received message:", message)
    # Logic to encrypt and send the message to serverKey.py goes here
    return "Message sent to server", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
