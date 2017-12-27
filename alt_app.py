import falcon
from pymongo import MongoClient
import json
import pandas as pd
from datetime import datetime
import re
from wsgiref import simple_server  

client = MongoClient('localhost',27017)
db = client['user_data']
user = db.posts

def get_work_experience(user):
    first_name = input('Enter first name: ')
    output_dict_list = []
    output_dict = {}
    for i in list(user.find({'FirstName':first_name})):
        output_dict_list.append({'FirstName': first_name, 'LastName':i['LastName'], 'FirstWorkExperience':i['CareerTimeline']['WorkExperience'][-1]['title']})
    if output_dict_list == []:
        return None
    else:
        return json.dumps(output_dict_list)

class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.body = get_work_experience(user)
        if resp.body == None:
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200
        
# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/users', things)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
