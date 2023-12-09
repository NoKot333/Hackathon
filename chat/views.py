from django.http import HttpResponse
from django.shortcuts import render
import socket

def home(request):
    if (request.META['SERVER_PORT']=="9322"):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("127.0.0.1",9323)
        server_socket.bind(server_address)
        server_socket.listen(1)
        print('Ждем подключения...')
        client_socket, client_address = server_socket.accept()
        print('Подключено', client_address)
        data = client_socket.recv(1024)
        print('Получено:', data.decode('utf-8'))
        message = "Привет, клиент"
        client_socket.sendall(message.encode('utf-8'))
        client_socket.close()
        return render(
            request,
            'server/index.html'
        )
    else:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 9323)
        client_socket.connect(server_address)
        message = "Привет, сервер"
        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(1024)
        print('Получено:', data.decode('utf-8'))
        client_socket.close()
        return render(
            request,
            'client/home/index.html'
        )