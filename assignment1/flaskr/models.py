import os
import json
import bcrypt
import uuid
from flask import request

class KomradeConfig:
    def __init__(self, name):
        self.config_file = os.path.join(os.path.dirname(__file__), "../" + name + ".json")

        if not os.path.exists(self.config_file):
            open(self.config_file, "w").write("{}")

    def read(self):
        return json.loads(open(self.config_file, "r").read())

    def write(self, data):
        with open(self.config_file, 'w') as fh:
            fh.write(json.dumps(data))

##Check to see if username is in database otherwise write new user in database
def registerUser(username, password):
    komrade = KomradeConfig("user")
    data = komrade.read()      
    if username in data:
        return 400
    else:
        data[username] = password
        komrade.write(data)
        return 0
    
##Check to see if username is in database
def validateUser(username, password):
    komrade = KomradeConfig("user")
    data = komrade.read()
    if username not in data or data[username] != password:
        return 403
    else:     
        return 0

    return None
