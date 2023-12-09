# client.py
import socket
import sys
import pickle
from util.HashAlgo import HashAlgo
from util.Operations import Operations
from util.RSA import RSA
from util.SAES import SAES


class Client:
    def __init__(self):
        print("[ЗАПУСКАЕТСЯ] Клиент запускается...")
        self.PORT = 5050
        # Local IP Addess of the host
        self.SERVER_IP = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print(f'[Подключение] Клиент пытается подключиться {self.SERVER_IP}...')
        self.client_socket.connect(self.ADDR)

        print(f'[Подключено] Установлено защищенное соединение с сервером.')

    def inputMessage(self):
        print("Введите ваше сообщение для отправки на сервер:")
        self.message = input()

    def inputKey(self):
        #print("Введите секретный ключ. Значение должно быть в диапазоне от 0 до {}, так как размер ключа равен {}:".format(
        #    2 ** SAES.key_size - 1, SAES.key_size))
        self.key = 512
        if (self.key < 0) or (self.key > (2 ** SAES.key_size - 1)):
            print("Follow the rules for the key")
            exit(1)

    def inputKeyParameters(self):
        self.p, self.q, self.e = 50411,46049,65537

    def generateClientKeys(self):
        self.private_key, self.public_key = RSA.generateKeys(
            self.p, self.q, self.e)

    def recieveMsg(self):
        msg = self.client_socket.recv(1024)
        msg = pickle.loads(msg)
        return msg

    def sendMsg(self, data):
        data = pickle.dumps(data)
        self.client_socket.send(data)

    def _ciphertextHex(self, ciphertext):
        ciphertext_hex = []
        for i in ciphertext:
            ciphertext_hex.append("{:04x}".format(int(i, 2)))
        return ciphertext_hex

    def workFlow(self):
        # Encrypting secret key
        encrypted_secret_key = RSA.encrypt(
            self.server_public_key, str(self.key))
        print("\nЗашифрованный секретный ключ:", RSA.printHexList(encrypted_secret_key))

        # Creating ciphertext
        print("\n[Клиентское] шифрование...")
        subkeys = SAES.generate_subkeys(self.key)
        ciphertext = SAES.encrypt(self.message, subkeys)
        ciphertext_hex = self._ciphertextHex(ciphertext)
        print('Зашифрованный текст:', ''.join(ciphertext_hex))

        # Generating digest
        hash_code = HashAlgo.generateHashCode(message=self.message)
        print(f"\nпрофиль сообщения {hash_code}")

        # Creating digital signature using hash code
        client_sign = RSA.sign(self.private_key, hash_code)
        print("Подпись клиента:", RSA.printHexList(client_sign))

        # arranging datas to be send to server
        data = {'secret_key': encrypted_secret_key, 'ciphertext': ciphertext_hex,
                'client_signature': client_sign, 'client_public_key': self.public_key, 'padded': SAES.is_padded}

        # Sending data to server
        self.sendMsg(data)

        self.client_socket.close()


client_obj = Client()
client_obj.connect()
print("\n--------------Code by ЧОКОПАЙ (09.12.2023)--------------\n")

client_obj.inputMessage()
client_obj.inputKey()
client_obj.inputKeyParameters()

# Now verify key parameters
is_verified = RSA.verifyParameters(client_obj.p, client_obj.q, client_obj.e)
if not is_verified:
    client_obj.inputKeyParameters()

# Generate public and private keys
client_obj.generateClientKeys()

print("Вы хотите запросить у сервера его открытый ключ? Y или N")
res = input()
if res.lower() == 'y':
    # Requesting server for it's public key
    print("[Запрашивает] открытый ключ сервера...")
    client_obj.sendMsg("Y")

    # Recieving server's public key
    client_obj.server_public_key = client_obj.recieveMsg()

    print("Открытый ключ сервера получен!")

    ##############################################################################

    # Workflow
    client_obj.workFlow()

else:
    print("[Клиент] Закрываем соединение...")
    client_obj.client_socket.close()