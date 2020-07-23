from bottle import db_dir
import json
from numpy import random as rd

#TODO using bottle.define_path_vars() to define path
captionstory_dir = 'captionstory'
storypath = f'{db_dir}/{captionstory_dir}/story.json'
namepath = f'{db_dir}/{captionstory_dir}/name.json'

with open(storypath,'r') as story_json:
    STORIES = json.load(story_json)
    story_json.close()

with open(namepath,'r') as name_json:
    NAMES = json.load(name_json)
    name_json.close()

def get_caption(bottle_name, person_name=None):
    if person_name:
        return rd.choice(STORIES).format(person_name,bottle_name)
    else:
        return rd.choice(STORIES).format(rd.choice(NAMES)['first_name'],bottle_name)