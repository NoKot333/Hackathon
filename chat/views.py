from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    if (request.META['SERVER_PORT']=="9322"):
        return render(
            request,
            'server/server.html'
        )
    else:
        return render(
            request,
            'client/home/index.html'
        )
def chat(request):
    return render(
        request,
        'client/home/chat.html'
    )
def login(request):
    return render(
        request,
        'client/home/login.html'
    )