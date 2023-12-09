import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.клиенты = {}

        # Генерация ключа для AES
        self.key_aes = get_random_bytes(16)
        
        # Генерация ключей для RSA
        key_pair = RSA.generate(2048)
        self.public_key = key_pair.publickey().export_key()
        self.private_key = key_pair.export_key()

    def client(self, client_socket, adress):
        # Инициализация объектов шифрования
        cipher_aes = AES.new(self.key_aes, AES.MODE_EAX)

        # Отправка открытого ключа RSA клиенту
        client_socket.send(self.public_key)

        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Соединение с {adress} закрыто.")
                del self.client[adress]
                break

            # Расшифровка сообщения с использованием AES
            nonce, tag, ciphertext = data.split(b'|')
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)

            message = data.decode('utf-8')
            print(f"Получено зашифрованное сообщение от {adress}: {message}")

    def start(self):
        print("Сервер слушает соединения...")
        while True:
            client_socket, adress = self.server_socket.accept()
            print(f"Принято соединение от {adress}")
            self.client[adress] = client_socket
            flow_client = threading.Thread(target=self.client, args=(client_socket, adress))
            flow_client.start()

if __name__ == "__main__":
    Server = Server("127.0.0.1", 9323)
    Server.start()