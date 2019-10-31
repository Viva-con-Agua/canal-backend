###
# Mattermost Api Class. Call the Mattermost Api 
# https://api.mattermost.com/
##



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
        self.urls['get_user_email'] = settings.MM['ADDRESS'] + '/users/email'


    ## 
    # Implements the login and logout for the admin account
    ## 

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


    ##
    # User Contain function for api/v4/users
    ##

    ## Create Mattermost User
    # required user as json and access_token
    # return response of MattermostApi function 'Create a user' 
    def create_user(self, user, access_token):
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
        return response
    
    ## Get Mattermost user by email
    # required email and access_token
    # return response of MattermostApi function 'Get user by email'
    def get_user_by_email(self, email, access_token):
        headers = self.headers
        headers['Authorization'] = 'Bearer ' + access_token
        url = settings.MM['ADDRESS'] + '/api/v4/users/email/' + email
        try: 
            response = requests.get(
                    url,
                    headers=headers
                    )
        except requests.exceptions.MissingSchema as e:
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None
        return response
    
    ##
    # Team function for /api/v4/teams requests
    ##
    
    ## List teams
    # required access_token
    # return response of MattermostApi function 'Get Teams'
    def list_teams(self, access_token):
        headers = self.headers
        headers['Authorization'] = 'Bearer ' + access_token
        url = settings.MM['ADDRESS'] + '/teams' 
        try:
            response = requests.get(
                url,
                headers=headers
                    )
        except requests.exceptions.MissingSchema as e:
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None
        return response
    
    ## get team by name
    # required name and access_token
    # return response of MattermostApi function 'Get a team by name'
    def get_team_by_name(self, name, access_token):
        headers = self.headers
        headers['Authorization'] = 'Bearer ' + access_token
        print(name)
        url = settings.MM['ADDRESS'] + '/api/v4/teams/name/' + name
        try: 
            response = requests.get(
                    url,
                    headers=headers
                    )
        except requests.exceptions.MissingSchema as e:
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None
        return response

    ## join user to a team by id
    # required user_id, team_id and access_token
    # return response of MattermostApi function 'Add user to team'
    def join_user_team_by_id(self, user_id, team_id, access_token):
        headers = self.headers
        headers['Authorization'] = 'Bearer ' + access_token
        data = {'team_id': team_id, 'user_id': user_id}
        url = settings.MM['ADDRESS'] + '/api/v4/teams/' + team_id + '/members' 
        try:
            response = requests.post(
                url,
                headers=headers,
                data= json.dumps(data)
                    )
        except requests.exceptions.MissingSchema as e:
            logger.error(e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None
        return response
