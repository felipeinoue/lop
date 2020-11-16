from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *

def index(request):
    # check method
    if request.method == 'GET':

        # if user not authenticated render login.html
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        
    return render(request, "lop/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "lop/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "lop/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lop/register.html", {
                "message": "Passwords must match."
            })

        # check if email is already taken
        try:
            user = User.objects.get(email=email)
            return render(request, "lop/register.html", {
                "message": "Email address already taken."
            })
        except:
            pass

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.lop_username = username
            user.save()
        except:
            return JsonResponse({"error": "There was a problem creating your account, contact the administrator."}, status=404)

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lop/register.html")


########### APIs ###########


def api_lops(request):

    # Check request
    if request.method == "POST":

        # start variables
        data = json.loads(request.body)
        project_name = data.get('project')

        # check if project already exists
        try:
            project = Project.objects.get(project=project_name)
            return JsonResponse({"error": "Project name is alread used."}, status=400)
        except:
            pass

        # attempt to create new project
        try:
            project = Project(project=project_name)
            project.save()
            return JsonResponse({"message": "Project succesfully created."}, status=201)
        except:
            return JsonResponse({"error": "There was an error creating your project."}, status=400)

    # Method invalid
    else:
        return JsonResponse({"error": "Invalid method."}, status=400)