from django.conf import settings
import logging
logger = logging.getLogger(__name__)
import json
from mattermost.mattermostApi import MattermostApi
from mattermost.utils import Utils

class Service:

    def __init__(self):
        self.dummy = "dummy"
    
    # create user with given password
    def create_employee(self, user_json, password):
        # initial MattermostApi
        mattermostApi = MattermostApi()
        utils = Utils()
        ##
        # Login Mattermost user
        ##
        
        # use mattermostApi to get access_token
        access_token = mattermostApi.login()
        if access_token == None:
            return None
        ##
        # Create Mattermost User
        ##
        
        # use utils for build a mattermost user model based on the pool profile
        mm_user = utils.build_user_model(user_json, password)
        # use mattermostApi to create a user. If any error is detected, the function return None
        result_user_create = mattermostApi.create_user(mm_user, access_token)
        if result_user_create == None:
            return None
        
        ##
        # Join employee to entity team
        ##
        
        # Check if the user is employee and return the entity or None
        entity = utils.get_entity_employee(user_json)
        if entity is not None:
            ##
            # Handels user request
            ##
            # get the user_id by email
            user_response = mattermostApi.get_user_by_email(user_json['profiles'][0]['email'], access_token)
            if user_response.status_code == 200:
                user = json.loads(user_response.text)
            else:
                logger.error(utils.error_response(user_response, 'get_user_by_email'))
                user = None

            ##
            # Handels team request
            ##
            # get teams by entity name

            # global team for all employee
            global_team_response = mattermostApi.get_team_by_name(settings.ENTITIES['global'], access_token)
            if team_response.status_code == 200:
                global_team = json.loads(global_team_response.text)
            else:
                logger.error(utils.error_response(global_team_response, 'get_team_by_name'))
                global_team = None
            
            # entity team for employee entity
            team_response = mattermostApi.get_team_by_name(entity, access_token)
            # status_code response a team
            if team_response.status_code == 200:
                team = json.loads(team_response.text)
            else:
                logger.error(utils.error_response(team_response, 'get_team_by_name'))
                team = None

            # if there is an user and the global team has found join user global there is an team, match both via id
            if user is not None and global_team is not None:
                mattermostApi.join_user_team_by_id(user['id'], global_team['id'])
                # if entity found, join entity team
                if team is not None:
                    mattermostApi.join_user_team_by_id(user['id'], team['id'], access_token)
        ##
        # Logout mattermost admin
        ##

        mattermostApi.logout(access_token)
        return result_user_create
    
    def has_account(self, email):
        # initial MattermostApi
        mattermostApi = MattermostApi()
        # get Mattermost access_token via login api request
        access_token = mattermostApi.login()
        if access_token == None:
            return None
        # get account via request
        result = mattermostApi.get_user_by_email(email, access_token)
        if result == None:
            return None
        mattermostApi.logout()
        return result


                


    


            
