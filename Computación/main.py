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
file='https://raw.githubusercontent.com/linagiraldom/Parcial2/main/Computación/static/data/FACom_art.json'


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
	"""
    Esta aplicación permite consultar los artículos asociados a una institución basándose en una palabra clave,
    la cual es ingresada como un parámetro de URL.
	
	Ejemplo de uso
	--------------

	Ingresar por url: http://127.0.0.1:8000/ devolverá una lista de todos los artículos que estén asociados a
	una institución en la base de datos.

	Ingresar parámetro por URL: http://127.0.0.1:8000/?affiliation=nombre%20de%20institución devolverá todos
	los artículos donde al menos uno de los autores esté asociado a una institución que en su nombre lleve
	el valor del parámetro `affiliation`.

	El parámetro `affiliation` puede ser una palabra clave, como facom. No es case-sensitive, por lo que 
	http://127.0.0.1:8000/?affiliation=facom equivale a http://127.0.0.1:8000/?affiliation=FACom
    """
    
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
