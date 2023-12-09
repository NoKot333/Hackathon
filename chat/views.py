from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    if (request.META['SERVER_PORT']=="9322"):
        return render(
            request,
            'server/index.html'
        )
    else:
        return render(
            request,

            'client/home/chat.html'
        )