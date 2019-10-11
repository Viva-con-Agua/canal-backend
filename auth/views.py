from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
import requests


##
# Implementation of the Oauth based handshake for Pool²
# authentication.
##

# start pool login procedure for backend services request
# auth_code_url is request the authorization_code via redirect
def login_pool(request):
    auth_code_url = (
            settings.POOL_AUTH['HOST'] + 
            settings.POOL_AUTH['AUTH_SERVER'] + 
            '/oauth2/code/get?client_id=' + 
            settings.POOL_AUTH['CLIENT_ID'] +
            '&ajax=true&response_type=code&state=&redirect_uri=' +
            settings.POOL_AUTH['HOST'] +
            '/matter/auth/redirectUri/'
            )
    return HttpResponseRedirect(auth_code_url)
# redirectUri for handling token
def redirect_uri(request):
    # get authCode from queryString
    authCode = request.GET.get('code', 'value')
    # build url for request the access_token
    url = (
            settings.POOL_AUTH['HOST'] + 
            settings.POOL_AUTH['AUTH_SERVER'] + 
            '/oauth2/access_token?client_id=' +
            settings.POOL_AUTH['CLIENT_ID'] +
            '&ajax=true&grant_type=authorization_code&code=' + 
            authCode + 
            '&state=&redirect_uri=' + 
             settings.POOL_AUTH['HOST'] + 
            '/matter/auth/redirectUri/'
            )
    
    # request the access_token
    try:
        access_token_response = requests.get(url)
    except requests.exceptions.MissingSchema as e:
        return HttpResponse(e)
    except requests.exceptions.RequestException as e:
        return HttpResponse(e)
    
    # if status code 200 => get access_token
    # else status code 401 => response error
    if access_token_response.status_code == 200:
        try:
            tokenJson = json.loads(access_token_response.text)
            access_token = tokenJson['access_token']
        except KeyError:
            return HttpResponse('Error: no access_token')
    else: 
        return HttpResponse(access_token_response.text, status=401)
    
    # request user
    try:
        user_url = ( 
            settings.POOL_AUTH['HOST'] + 
            settings.POOL_AUTH['AUTH_SERVER'] + 
            '/oauth2/rest/profile?access_token=' + 
            access_token
            )
        user_response = requests.get(user_url)
    except requests.exceptions.MissingSchema as e:
        return HttpResponse(e)
    except requests.exceptions.RequestException as e:
        return HttpResponse(e)
    # bind access_token to session. Can now used in other views
    request.session['access_token'] = access_token
    return HttpResponse(user_response.text)
    
    
