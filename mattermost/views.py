from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import json
import requests
# Create your views here.


##
# Mattermost requests for handling user SignUp
##

def login_api():
    auth = {
            'login_id': settings.MM['ID'],
            'password': settings.MM['PASSWORD']
        }
    headers = {'Content-Type': 'application/json'}
    url = settings.MM['ADDRESS'] + '/api/v4/users/login'

    try:
        r = requests.post(
                url,
                headers=headers,
                data=json.dumps(auth)
                )
        token = r.headers['token']
        return token
    except requests.exceptions.MissingSchema as e:
        return HttpResponse(e)
    except requests.exceptions.RequestException as e:
        return HttpResponse(e)

def post_user(user, token):
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = 'Bearer ' + token
    url = settings.MM['ADDRESS'] + '/api/v4/users'
    try:
        r = requests.post(
            url,
            headers=headers,
            data=json.dumps(user)
            )
        return r.text
    except requests.exceptions.MissingSchema as e:
        return HttpResponse(e)
    except requests.exceptions.RequestException as e:
        return HttpResponse(e)

def logout_api(token):
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = 'Bearer ' + token
    url = settings.MM['ADDRESS'] + '/users/logout'
    try:
        r = requests.post(
            url,
            headers=headers,
            data={}
                )
        return r.text
    except requests.exceptions.MissingSchema as e:
        return HttpResponse(e)
    except requests.exceptions.RequestException as e:
        return HttpResponse(e)

# required user as json and password string
def build_user_model(user_json, password):
    mm_user = {}
    mm_user['email'] = user_json['profiles'][0]['email']
    mm_user['password'] = password
    mm_user['auth_data'] = user_json['profiles'][0]['email']
    mm_user['auth_service'] = 'email'
    mm_user['last_name'] =  user_json['profiles'][0]['supporter']['lastName']
    mm_user['first_name'] = user_json['profiles'][0]['supporter']['firstName']
    mm_user['props'] = {
            'pool_id': user_json['id']
            }
    return mm_user

def create_user(user, password):
    # build Mattermost user_model
    user_json = json.loads(user)
    mm_user = build_user_model(user_json, password)
    # post usermode to mattermost api
    access_token = login_api() # get access_token
    response = post_user(mm_user, access_token) # post user to api with required token
    logout_api(access_token)
    return response


##
# get user via PoolApi with access_token
##
def user_request(access_token):
    try:
        pUrl = ( 
            settings.POOL_AUTH['HOST_INT'] + 
            settings.POOL_AUTH['AUTH_SERVER'] + 
            '/oauth2/rest/profile?access_token=' + 
            access_token
            )
        p = requests.get(pUrl)
    except requests.exceptions.MissingSchema as e:
        return HttpResponse(e)
    except requests.exceptions.RequestException as e:
        return HttpResponse(e)
    return json.loads(p.text)


@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        password = body['password']
        
        if 'access_token' not in request.session:
            error = '{"status": "user not authenticated"}'
            return HttpResponse(error, 401)
        else:
            access_token = request.session['access_token']
            try:

                pUrl = ( 
                    settings.POOL_AUTH['HOST_INT'] + 
                    settings.POOL_AUTH['AUTH_SERVER'] + 
                    '/oauth2/rest/profile?access_token=' + 
                    access_token
                    )
                p = requests.get(pUrl)
            except requests.exceptions.MissingSchema as e:
                return HttpResponse(e)
            except requests.exceptions.RequestException as e:
                return HttpResponse(e)
            output = create_user(p.text, password)
            return HttpResponse(output)
        return HttpResponse(password)
    else:
        error = '{"Error": "only POST request supportet on this url"}'
        response = HttpResponse(error, status=405)
        return HttpResponse('{"Error"}')
    

