from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.conf import settings
from mattermost.service import Service
from canal.dropsApi import DropsApi
import json
import requests
# Create your views here.

service = Service()

@require_http_methods(["POST"])
def addEntity(request):
    body = json.loads(request.body)
    try: 
        name = body['name']
    except KeyError as e:
        return HttpResponse("{'Error': 'required key name'}", status=400)
    try:
        team = body['team']
    except KeyError as e:
        return HttpResponse('{"Error": "required key team"}', status=400)
    entity = Entity.objects.create(name=name)
    try:
        entity.save()
    except django.db.IntegrityError as e:
        return HttpResponse('{"status": "entry exists"}', status=201)
    return HttpResponse('{"status": "successfully created Entry"}', status=200)
    




@csrf_exempt


@require_http_methods(["GET"])
def hasAccount(request):
    # check if the user has an access_token
    if 'access_token' not in request.session:
        error = '{"status": "user not authenticated"}'
        return HttpResponse(error, status=401)

    # initial dropsApi and get profile
    dropsApi = DropsApi()
    profile = dropsApi.get_profile(request.session['access_token'])
    
    # if None there is an internal Error, so return 500
    if profile == None:
        return HttpResponse('{"Error": "Internal Server Error"}', status=500)
    # if status_code == 200, we have a profile
    elif profile.status_code == 200:
        # user = json.loads(profile.text)
        #mm_user_email = user['profiles'][0]['email']
        result = service.has_account(json.loads(profile.text)['profiles'][0]['email'])
        if result == None:
            return HttpResponse('{"Error": "Internal Server Error"}', status=500)
        else:
            return HttpResponse(result.text, status=result.status_code)
    else:
        return HttpResponse(profile.text, status=profile.status_code)

@csrf_exempt
@require_http_methods(["POST"])
def createEmployee(request):
    # get password from body
    body = json.loads(request.body)
    try:
        password = body['password']
    except KeyError as e:
        return HttpResponse("{'Error': 'required key password'}", status=400)
    # check if access_token is in request session
    if 'access_token' not in request.session:
        # return 401
        error = '{"status": "user not authenticated"}'
        return HttpResponse(error, 401)
    
    # request user profile via dropsApi 
    access_token = request.session['access_token']
    dropsApi = DropsApi()
    profile = dropsApi.get_profile(access_token)
    # 
    if profile == None:
        return HttpResponse("{'Error':'Internal Server Error'}", status=500)
     
    elif profile.status_code == 200:
        service = Service()
        result = service.create_employee(json.loads(profile.text), password)
        if result == None:
            return HttpResponse("{'Error':'Internal Server Error'}", status=500)
        else:
            return HttpResponse(result.text, status=result.status_code)
    else:
        return HttpResponse(profile.text, status=profile.status_code)

