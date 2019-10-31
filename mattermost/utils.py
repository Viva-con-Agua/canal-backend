
from django.conf import settings
import json

##
# utils for some complexer processes 
#
class Utils:
    def __init__(self):
        self.teams = settings.ENTITIES
    

    # required user as json and password string
    # return mattermost user
    def build_user_model(seld, user_json, password):
        mm_user = {}
        mm_user['email'] = user_json['profiles'][0]['email']
        mm_user['password'] = password
        mm_user['auth_data'] = user_json['profiles'][0]['email']
        mm_user['auth_service'] = 'email'
        
        if 'lastName' in user_json['profiles'][0]['supporter']:
            mm_user['last_name'] =  user_json['profiles'][0]['supporter']['lastName']
        else:
            mm_user['last_name'] = ""
        
        if 'firstName' in user_json['profiles'][0]['supporter']:
            mm_user['first_name'] = user_json['profiles'][0]['supporter']['firstName']
        else:
            mm_user['first_name'] = ""
        mm_user['props'] = {
            'pool_id': user_json['id']
            }
        return mm_user
    
    # get entity of an user 
    # entity is coded in roles
    def get_entity_employee(self, user_json):
        #get roles
        roles = user_json['roles']
        # check if an value of key role is employee
        for role in roles:
            if 'employee' in role['role']:
                # search the entity in roles and return if there is one 
                # else return None
                for r in roles:
                    if r['role'] in self.teams:
                        return self.teams[r['role']]
                return None
            else:
                return None
    


    def error_response(self, res, func):
        error = '{}\n{}\r\n{}\r\n\r\n{}'.format(
            'Func: ' + func,
            str(res.status_code) + ' ' + res.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
            res.text,
            )
        return(error)

