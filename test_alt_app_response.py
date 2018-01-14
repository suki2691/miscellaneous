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
import pytest

mongo.connect('user_data',port=27017)

# first_name_true = ['Jarrah','Hassan','Emer']


class TestThings(testing.TestBase):
    def before(self):
        things = ThingsResource()
        self.api.add_route('/users', things)

    def test_true(self):
        body = self.simulate_request('/users?firstname=Jarrah','GET')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(body.json, get_work_experience('Jarrah'))
