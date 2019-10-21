from django.conf import settings

import logging
logger = logging.getLogger(__name__)

import json
import requests

class DropsApi:
    def __init__(self):
        self.urls = {}
        self.urls['get_profile'] = ( 
                settings.POOL_AUTH['HOST_INT'] + 
                settings.POOL_AUTH['AUTH_SERVER'] + 
                '/oauth2/rest/profile?access_token='
                )
    ## get access_token from drops via authorization_code
    def get_access_token(self, code):
        url = (
            settings.POOL_AUTH['HOST_INT'] + 
            settings.POOL_AUTH['AUTH_SERVER'] + 
            '/oauth2/access_token?client_id=' +
            settings.POOL_AUTH['CLIENT_ID'] +
            '&ajax=true&grant_type=authorization_code&code=' + 
            code + 
            '&state=&redirect_uri=' + 
             settings.POOL_AUTH['HOST'] + '/' +
             settings.CONTEXTPATH +
            'auth/redirectUri/'
            )
        try:
            response = requests.get(url)
            return response
        except requests.exceptions.MissingSchema as e:
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None

    
    ## get profile from drops via access_token
    def get_profile(self, access_token):
        try:
            response = requests.get(self.urls['get_profile'] + access_token)
            return response
        except requests.exceptions.MissingSchema as e:
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None

