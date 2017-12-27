import falcon
from pymongo import MongoClient
import json
import pandas as pd
from datetime import datetime
import re  

def experience(parsed):
    new_data = parsed['experience']
    experience_data ={k.replace('.','').replace('/',' '):v for k,v in new_data.items()}
#     print(experience_data)
    k = 0
    exps = []
    for i in experience_data.keys():
        exp = {}
        exp['id'] = k
        exp['title'] = i
        if experience_data[i]:
            if ' to ' in experience_data[i]:
                exp['startdate'] = experience_data[i].split(' to ')[0]
                exp['enddate'] = experience_data[i].split(' to ')[1]
            elif ' a ' in experience_data[i]:
                exp['startdate'] = experience_data[i].split(' a ')[0]
                exp['enddate'] = experience_data[i].split(' a ')[1]
            elif ' bis ' in experience_data[i]:
                exp['startdate'] = experience_data[i].split(' bis ')[0]
                exp['enddate'] = experience_data[i].split(' bis ')[1]
        else:
            exp['startdate'] = 'None'
            exp['enddate'] = 'None'
        k += 1
        exps.append(exp)
    return exps

def career_timeline(parsed,id):
    career = {}
    career['id'] = id
    career['WorkExperience'] = experience(parsed)
    if 'education' in parsed.keys():
        new_parsed = {k.replace(".", ""):v for k,v in parsed['education'].items()}
        career['EducationExperience'] = new_parsed
    else:
        career['EducationExperience'] = {}
    career['Location'] = parsed['location']
    return career

def users(data):
    user = {}
    page = open("CareerTimelines/"+data['CareerTimeline'], 'r')
    parsed = json.loads(page.read())
    user['id'] = data['Id']
    user['FirstName'] = data['First Name']
    user['LastName'] = data['Last Name']
    user['Email'] = data['Email']
    user['CareerTimeline'] = career_timeline(parsed,data['Id'])
    return user

excel_data = pd.read_excel('Database.xlsx').reset_index()
excel_data.columns = ['Id', 'First Name', 'Last Name', 'Email', 'CareerTimeline']
user_dict = excel_data.to_dict('records')

client = MongoClient('localhost', 27017)
client.test_database
db = client['user_data']
user_collection = db['users']
user = db.posts
for i in user_dict:
    user.insert_one(users(i))
