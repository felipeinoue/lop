from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# from .models import *

def index(request):

    return render(request, "lop/index.html")
