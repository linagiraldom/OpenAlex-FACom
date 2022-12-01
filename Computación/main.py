'''
$ sudo pip3 install fastapi
$ pip3 install uvicorn[standard]
$ uvicorn main:app --reload
'''
from typing import Optional

from fastapi import FastAPI

from starlette.responses import FileResponse ###
from starlette.staticfiles import StaticFiles ###

import requests

import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") ###

#file='https://raw.githubusercontent.com/restrepo/OpenAlexGroup/main/data/calificaciones.json'
file='https://raw.githubusercontent.com/linagiraldom/Parcial2/main/static/data/FACom_art.json'


#JSON SCHEME
#[{"student_id": str,
# "Evaluation 1":{"value": int,
#                 "%": int,
#                 "Description": str
#                 }, 
# ...
# }
#]

@app.get("/")
def read_item(affiliation	: str = ""):
    '''
    You can write the API documentation here:
    
    For example: 
    
    USAGE: http://127.0.0.1:8000/?student_id=1113674432
    '''
    
    #Real time JSON file
    r=requests.get(file)
    db=[r.json()] # Agregar []
    
    #new_db=[ (d['display_name'][str(k)],d['authorships'][str(k)][0].get('raw_affiliation_string')) for d in db for k in range(len(d['display_name'])) if d['authorships'][str(k)][0].get('raw_affiliation_string') == affiliation ]
    #new_db=list(set([ (d['display_name'][str(k)],d['authorships'][str(k)][0].get('raw_affiliation_string')) for d in db for k in range(len(d['display_name'])) if (d['authorships'][str(k)][0].get('raw_affiliation_string') != None and affiliation.lower() in d['authorships'][str(k)][0].get('raw_affiliation_string').lower()) ]))
    new_db= {d['display_name'][str(k)]:d['authorships'][str(k)][0].get('raw_affiliation_string') for d in db for k in range(len(d['display_name'])) if (d['authorships'][str(k)][0].get('raw_affiliation_string') != None and affiliation.lower() in d['authorships'][str(k)][0].get('raw_affiliation_string').lower()) }
    new_db = [d for d in new_db.items()]
    f=open('static/data/filtered.json','w') #***
    json.dump(new_db,f)
    f.close()
    #with open(file) as json_file:
    #   db=json.load(json_file)
    
#    if not student_id:
#        return FileResponse('index.html')
#    else:
#        return FileResponse('index.html')
    return FileResponse('index.html') ###
