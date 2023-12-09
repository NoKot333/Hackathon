import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

class Client:
    def __init__(self, server_ip, server_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))

        # Получение открытого ключа RSA от сервера
        self.public_key_server = self.client_socket.recv(2048)

        # Генерация ключа для AES
        self.key_aes = get_random_bytes(16)

        threading.Thread(target=self.get_message).start()

    def get_message(self):
        # Инициализация объектов шифрования
        cipher_aes = AES.new(self.key_aes, AES.MODE_EAX)
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(self.public_key_server))

        while True:
            data = self.client_socket.recv(1024)
            if not data:
                print("Сервер закрыл соединение.")
                break

            # Расшифровка сообщения с использованием AES
            nonce, tag, ciphertext = data.split(b'|')
            data = cipher_aes.decrypt_and_verify(ciphertext, tag, nonce)

            message = data.decode('utf-8')
            print(f"Получено зашифрованное сообщение: {message}")

    def post_message(self, message):
        # Инициализация объектов шифрования
        cipher_aes = AES.new(self.key_aes, AES.MODE_EAX)
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(self.public_key_server))

        # Шифрование сообщения с использованием AES
        ciphertext, tag, nonce= cipher_aes.encrypt_and_digest(message.encode('utf-8'))

        # Шифрование ключа AES с использованием открытого ключа RSA сервера
        encrypted_key_aes = cipher_rsa.encrypt(self.key_aes)

        # Отправка зашифрованного ключа AES и зашифрованного сообщения серверу
        self.client_socket.send(encrypted_key_aes + b'|' + b'|'.join([nonce, tag, ciphertext]))

if __name__ == "__main__":
    Client = Client("127.0.0.1", 9323)
    while True:
        message = input("Введите сообщение: ")
        Client.post_message(message)
