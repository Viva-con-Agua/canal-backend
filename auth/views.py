from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
from canal.dropsApi import DropsApi
import json
import requests


##
# Implementation of the Oauth based handshake for Pool²
# authentication.
##

# start pool login procedure for backend services request
# auth_code_url is request the authorization_code via redirect
@require_http_methods(["GET"])
def login_pool(request):
    auth_code_url = (
            settings.POOL_AUTH['HOST'] + 
            settings.POOL_AUTH['AUTH_SERVER'] + 
            '/oauth2/code/get?client_id=' + 
            settings.POOL_AUTH['CLIENT_ID'] +
            '&ajax=true&response_type=code&state=&redirect_uri=' +
            settings.POOL_AUTH['HOST'] + '/' +
            settings.CONTEXTPATH +
            'auth/redirectUri/'
            )
    return HttpResponseRedirect(auth_code_url)


# redirectUri for handling token
@require_http_methods(["GET"])
def redirect_uri(request):
    # get authorization_code from queryString
    code = request.GET.get('code', 'value')
    
    # init DropsApi
    dropsApi = DropsApi()
    # call access_token with authorization_code
    access_token_response = dropsApi.get_access_token(code)
    # if response == None return Internal Server Error
    if access_token_response == None:
        return HttpResponse({'Error': 'Internal Server Error'}, status=500)
    # if 200 store token in access_token
    elif access_token_response.status_code == 200:
        try:
            tokenJson = json.loads(access_token_response.text)
            access_token = tokenJson['access_token']
            request.session['access_token'] = access_token
        # if token empty return 401
        except KeyError:
            return HttpResponse({'Error': 'No access_token'}, status=401)
    # else return drops request
    else: 
        return HttpResponse(access_token_response.text, status=access_token_response.status_code)
    # store token in session
    # request profile and handle response
    profile = dropsApi.get_profile(access_token)
    if profile == None:
        return HttpResponse({'Error': 'Internal Server Error'}, status=500)
    else:
        return HttpResponse(profile.text, status=profile.status_code)
