from django.conf import settings
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
import json
import requests

class MattermostApi:

    def __init__(self):

        # init login credentials used for mattermost api token
        self.auth = {
            'login_id': settings.MM['ID'],
            'password': settings.MM['PASSWORD']
        }
        # init headers used for mattermost api request
        self.headers = {'Content-Type': 'application/json'}
        
        # define urls for the mattermost api
        self.urls = {}
        self.urls['login'] = settings.MM['ADDRESS'] + '/api/v4/users/login'
        self.urls['create_user'] = settings.MM['ADDRESS'] + '/api/v4/users'
        self.urls['logout'] = settings.MM['ADDRESS'] + '/users/logout'


    ## Login
    # Get mattermost api token.
    # If auth is correct return token 
    # else return None for Internal Server Error
    def login(self):
        try:
            r = requests.post(
                self.urls['login'],
                headers=self.headers,
                data=json.dumps(self.auth)
                )
            if r.status_code == 200:
                token = r.headers['token']
                return token
            else:
                logger.error(r.text)
                return None
        except requests.exceptions.MissingSchema as e:
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None
    
    ## Create Mattermost User
    # required user as json and mattermost token
    # return mattermost status_text

    def create_user(self, user):
        
        # get access token via login function
        access_token = self.login()
        # if access_token == None return None for Internal Server Error
        if access_token == None:
            return None

        # else request create_user url
        else:
            # create headers
            headers = self.headers
            headers['Authorization'] = 'Bearer ' + access_token
            
            # try request with create_user url
            try:
                response = requests.post(
                    self.urls['create_user'],
                    headers=headers,
                    data=json.dumps(user)
                )
            except requests.exceptions.MissingSchema as e:
                logger.error(e)
                return None
            except requests.exceptions.RequestException as e:
                logger.error(e)
                return None
            # logout mattermost admin
            self.logout(access_token)
        
            return response

    
    ## Logout Mattermost Admin
    # return status_text
    def logout(self, token):
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
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None

    # required user as json and password string
    # return mattermost user
    def build_user_model(seld, user_json, password):
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
