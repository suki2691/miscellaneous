import falcon
from pymongo import MongoClient
import json
import pandas as pd
from datetime import datetime
import re
from wsgiref import simple_server
import mongoengine as mongo
from mongo_data import User, Experience, Education, CareerTimeline
from falcon import testing
from alt_app import ThingsResource, get_work_experience

mongo.connect('user_data',port=27017)

# first_name_false = ['Suki','Ash','Kylie']

class TestThings(testing.TestBase):
    def before(self):
        things = ThingsResource()
        self.api.add_route('/users', things)

    def test_false(self):
        body = self.simulate_request('/users?firstname=Suki', decode='utf-8')
        self.assertEqual(self.srmock.status, falcon.HTTP_404)
