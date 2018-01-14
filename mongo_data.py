import falcon
from pymongo import MongoClient
import json
import pandas as pd
from datetime import datetime
import re
import mongoengine as mongo
import dateparser

# creating Mongo Engine models
class Experience(mongo.EmbeddedDocument):
    Id = mongo.ObjectIdField()
    Title = mongo.StringField()
    StartDate = mongo.DateTimeField()
    EndDate = mongo.DateTimeField()

class Education(mongo.EmbeddedDocument):
    Degree = mongo.StringField()
    StartDate = mongo.DateTimeField()
    EndDate = mongo.DateTimeField()

class CareerTimeline(mongo.Document):
    Id = mongo.ObjectIdField()
    WorkExperience = mongo.ListField(mongo.EmbeddedDocumentField('Experience'))
    EducationExperience = mongo.ListField(mongo.EmbeddedDocumentField('Education'))
    Location = mongo.StringField()

class User(mongo.Document):
    Id = mongo.ObjectIdField()
    FirstName = mongo.StringField(required=True)
    LastName = mongo.StringField(required=True)
    Email = mongo.StringField(required=True)
    CareerTimelines = mongo.ReferenceField(CareerTimeline)

#Extracting data from excel sheet data in MongoDB
excel_data = pd.read_excel('Database.xlsx').reset_index()
excel_data.columns = ['Id', 'First Name', 'Last Name', 'Email', 'CareerTimeline']
user_dict = excel_data.to_dict('records')

#Creating MongoDB
client = MongoClient('localhost', 27017)

client.test_database

db = client['user_data']

user_collection = db['users']

post = db.posts

if __name__ == '__main__':
    #Service route to format data to feed into MongoDB
    def load_user_data(parsed):
    #     print(parsed)
        new_data = parsed['experience']
        experience_data ={k.replace('.','').replace('/',' '):v for k,v in new_data.items()}

        exp = []
        if parsed['experience']:
            for i in experience_data.keys():

                experience = Experience(Title = i)
                if experience_data[i]:
                    if ' to ' in experience_data[i]:
                        experience.StartDate = dateparser.parse(experience_data[i].split(' to ')[0])
                        experience.EndDate = dateparser.parse(experience_data[i].split(' to ')[1])
                    elif ' a ' in experience_data[i]:
                        experience.StartDate = dateparser.parse(experience_data[i].split(' a ')[0])
                        experience.EndDate = dateparser.parse(experience_data[i].split(' a ')[1])
                    elif ' bis ' in experience_data[i]:
                        experience.StartDate = dateparser.parse(experience_data[i].split(' bis ')[0])
                        experience.EndDate = dateparser.parse(experience_data[i].split(' bis ')[1])
                else:
                    experience.StartDate = None
                    experience.EndDate = None
                exp.append(experience)
        else:
            experience = Experience()

        ed = []
        if 'education' in parsed.keys():
            if parsed['education']:
                new_parsed = {k.replace(".", ""):v for k,v in parsed['education'].items()}
                for i in new_parsed.keys():
                    education = Education(Degree=i)
                    if new_parsed[i]:
                        if ' to ' in new_parsed[i]:
                            education.StartDate = dateparser.parse(new_parsed[i].split(' to ')[0])
                            education.EndDate = dateparser.parse(new_parsed[i].split(' to ')[1])
                        elif ' a ' in new_parsed[i]:
                            education.StartDate = dateparser.parse(new_parsed[i].split(' a ')[0])
                            education.EndDate = dateparser.parse(new_parsed[i].split(' a ')[1])
                        elif ' bis ' in new_parsed[i]:
                            education.StartDate = dateparser.parse(new_parsed[i].split(' bis ')[0])
                            education.EndDate = dateparser.parse(new_parsed[i].split(' bis ')[1])
                        else:
                            education.StartDate = None
                            education.EndDate = None
                    ed.append(education)

            else:
                education = Education()

        else:
            education = Education()

        careerTimeline = CareerTimeline(WorkExperience=exp,EducationExperience=ed,Location=parsed['location'])
        careerTimeline.save(cascade=True)

        return careerTimeline

    for i in user_dict:
        mongo.connect('user_data',port=27017)
        page = open("CareerTimelines/"+i['CareerTimeline'], 'r')
        parsed = json.loads(page.read())
        careerTimeline = load_user_data(parsed)
        user = User(FirstName=i['First Name'],CareerTimelines=careerTimeline)
        user.LastName = i['Last Name']
        user.Email = i['Email']
        user.save()
