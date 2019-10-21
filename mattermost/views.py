from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.conf import settings
from mattermost.mattermostApi import MattermostApi
from canal.dropsApi import DropsApi
import json
import requests
# Create your views here.

@csrf_exempt

@require_http_methods(["POST"])
def createUser(request):
    # get password from body
    body = json.loads(request.body)
    password = body['password']
    # check if access_token is in request session
    if 'access_token' not in request.session:
        # return 401
        error = '{"status": "user not authenticated"}'
        return HttpResponse(error, 401)
    else:
        # request user profile via dropsApi 
        access_token = request.session['access_token']
        dropsApi = DropsApi()
        profile = dropsApi.get_profile(access_token)
        # 
        if profile == None:
            return HttpResponse({'Error':'Internal Server Error'}, status=500)
        else:
            if profile.status_code == 200:
                mattermostApi = MattermostApi()
                mm_user = mattermostApi.build_user_model(json.loads(profile.text), password)
                result = mattermostApi.create_user(mm_user)
                if result == None:
                    return HttpResponse({'Error':'Internal Server Error'}, status=500)
                else:
                    return HttpResponse(result.text, status=result.status_code)
            else:
                return HttpResponse(profile.text, status=profile.status_code)

