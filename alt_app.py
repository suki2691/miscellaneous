import falcon
from pymongo import MongoClient
import json
import pandas as pd
from datetime import datetime
import re
from wsgiref import simple_server
import mongoengine as mongo
from mongo_data import User, Experience, Education, CareerTimeline

mongo.connect('user_data',port=27017)

def get_work_experience(first_name):
    # first_name = input('Enter first name: ')
    output_dict_list = []
    output_dict = {}
    for i in User.objects(FirstName=first_name):
        output_dict_list.append({'FirstName': i.FirstName, 'LastName':i.LastName, 'FirstWorkExperience':i.CareerTimelines.WorkExperience[-1].Title})
    if output_dict_list == []:
        return None
    else:
        return json.dumps(output_dict_list)

class ThingsResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        first_name = req.params['firstname']
        resp.body = get_work_experience(first_name)
        if resp.body == None:
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200

# falcon.API instances are callable WSGI apps
app = falcon.API()
app = api = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/users', things)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
