import json
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

    # Check if method POST
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
            project = Project(
                project=project_name, 
                dateformat_id=1, #default dateformat DD/MM/YYYY 
                user_id=request.user.id)
            project.save()
        except:
            return JsonResponse({"error": "There was an error creating your project."}, status=400)

        # associate user as owner of the project
        try:
            member = Member(
                project=project,
                user_id=request.user.id,
                role_id=1 #1 = owner
            )
            member.save()
            return JsonResponse({"message": "Project succesfully created."}, status=201)
        except:
            return JsonResponse({"error": "There was an associating your user to the project."}, status=400)

    # check if method GET
    if request.method == 'GET':
        lop_lists = Member.objects.filter(user_id=request.user.id)

        # create list with all data
        ls = []
        for lop_list in lop_lists:
            ls.append(
                {
                    'project':lop_list.project.project,
                    'project_id':lop_list.project.id
                }
            )

        return JsonResponse(ls, safe=False, status=200)

    # Method invalid
    else:
        return JsonResponse({"error": "Invalid method."}, status=400)


def api_lop_details(request, project_id):

    # check method
    if request.method == 'GET':
        
        # get project
        try:
            project = Project.objects.get(pk=project_id)
        except:
            return JsonResponse({"error": "Project not found."}, status=404)

        # create dictionary with all data
        dictionary = {
            'project':project.project
        }

        # return json
        return JsonResponse(dictionary, safe=False, status=200)


    # Method invalid
    else:
        return JsonResponse({"error": "Invalid method."}, status=400)


def api_members_add(request):

    # Check if method POST
    if request.method == "POST":

        # start variables
        data = json.loads(request.body)
        project_id = data.get('project_id')
        emails = data.get('emails')

        # separate valid and invalid emails
        emails_valid = []
        emails_invalid = []
        for email in emails:

            # check if email exists in database
            try:
                user = User.objects.get(email=email)
            except:
                emails_invalid.append(email)
                continue

            # check if email is already added to the members of this project
            try:
                member = Member.objects.get(user=user, project_id=project_id)
                emails_invalid.append(email)
                continue
            except:
                pass

            # append to valid emails
            emails_valid.append(email)

        # attempt add valid emails to members
        emails_added = []
        for email_valid in emails_valid:

            # get user
            try:
                user = User.objects.get(email=email_valid)
            except:
                emails_invalid.append(email_valid)
                continue

            # add to the project members
            try:
                member = Member(
                    project_id=project_id,
                    user=user,
                    role_id=4 # default 4 (viewer)
                )
                member.save()
                emails_added.append(email_valid)
            except:
                emails_invalid.append(email_valid)


        # create list with all data
        dictionary = {
            'emails_added':emails_added,
            'emails_invalid':emails_invalid
        }

        return JsonResponse(dictionary, safe=False, status=200)

    # Method invalid
    else:
        return JsonResponse({"error": "Invalid method."}, status=400)


def api_members_table(request, project_id):

    # check if method GET
    if request.method == 'GET':

        # get all members of the requested project
        try:
            members = Member.objects.filter(project_id=project_id).order_by('user__lop_username')

        except:
            return JsonResponse({"error": "Project not found."}, status=404)

        # create list with all data
        ls = []
        for member in members:
            ls.append(
                {
                    'user_id':member.user.id,
                    'username':member.user.lop_username,
                    'email':member.user.email,
                    'role_id':member.role.id,
                    'role':member.role.role,
                    'weeklyemail':member.weeklyemail
                }
            )

        return JsonResponse(ls, safe=False, status=200)

    # Check if method POST
    if request.method == "POST":

        # start variables
        data = json.loads(request.body)
        user_id = data.get('user_id')

        # get user
        try:
            member = Member.objects.get(project_id=project_id, user_id=user_id)
        except:
            return JsonResponse({"error": "User not found."}, status=404)

        # check if data contain remove
        remove = data.get('remove')
        if remove:
            try:
                member.delete()
                return JsonResponse({"message": "User succesfully removed."}, status=200)
            except:
                return JsonResponse({"error": "There was a problem removing this user. Contact the administrator."}, status=400)

        # check if data contain role
        try:
            role_id = int(data.get('role_id'))
            member.role_id = role_id
            member.save()
        except:
            pass

        # check if data contain weeklyemail
        try:
            member.weeklyemail = data.get('weeklyemail')
            member.save()
        except:
            pass

        # create disctionary with all data
        dictionary = {
            'user_id':member.user.id,
            'username':member.user.lop_username,
            'email':member.user.email,
            'role_id':member.role.id,
            'role':member.role.role,
            'weeklyemail':member.weeklyemail
        }

        # return json
        return JsonResponse(dictionary, safe=False, status=200)

    # Method invalid
    else:
        return JsonResponse({"error": "Invalid method."}, status=400)


def api_roles(request):

    # check if method GET
    if request.method == 'GET':

        # get roles
        try:
            roles = Role.objects.all()
        except:
            return JsonResponse({"error": "There was an error retrieving the roles."}, status=400)

        # create list with all data
        dictionary = {}
        for role in roles:
            dictionary[f'{role.id}'] = f'{role.role}'

        # return json
        return JsonResponse(dictionary, safe=False, status=200)

    # Method invalid
    else:
        return JsonResponse({"error": "Invalid method."}, status=400)
