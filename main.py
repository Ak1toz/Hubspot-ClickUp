from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput, PublicObjectSearchRequest
from hubspot.crm.contacts.exceptions import ApiException

from database import SessionLocal
import models

app = FastAPI()
api_client = HubSpot(access_token='pat-na1-bfa3f0c0-426b-4f0e-b514-89b20832c96a')

class Contact(BaseModel):
    email: str = 'email@emailtest.com'
    firstname: str = 'Juan Camilo'
    lastname: str = 'Santander'
    phone: str = '08123456789'
    website: str = 'https://test.com'
    estado_clickup: str = 'pending'

class Apicall(BaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    endpoint: str
    params: Optional[Dict[str, Any]]
    result: Optional[str]

    class Config:
        orm_mode = True

db=SessionLocal()

def add_data_analyst(data: dict):
    
    new_data_analyst = models.Apicall(
            endpoint=data['endpoint'],
            params=data['params'],
            result=data['result']
        )

    db.add(new_data_analyst)
    db.commit()

    return new_data_analyst   



@app.get('/sync', tags=['sync'])
async def sync():
    x = 0
    data = {}

    try:
        all_contacts = api_client.crm.contacts.get_all()

        for contact in all_contacts:

            contact = contact.properties
            data[x] = contact
            x+=1

            # if contact['estado_clickup'] == 'pending':

            #     contact['estado_clickup'] = 'sync'
            #     simple_public_object_input = SimplePublicObjectInput(
            #         properties=contact
            #     )
            #     api_response = api_client.crm.contacts.basic_api.update(
            #         contact_id=contact_id,
            #         simple_public_object_input=simple_public_object_input
            #     )

                

        return {'message': 'sync completed', 'contacts': data}


    except ApiException as e:
        return {'message': "Exception when creating contact: %s\n" % e.body}


@app.post('/contact/add',status_code=201, tags=['contact'])
def add_contact(contact: Contact):

    contact = contact.dict()
    data = {}
    data['endpoint'] = 'contact/add method: POST'
    data['params'] = jsonable_encoder(contact)
    
    try:
        simple_public_object_input = SimplePublicObjectInput(
            properties=contact
        )
        api_response = api_client.crm.contacts.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )
        
        data['result'] = str(api_response.properties)

        # add_data_analyst(data)

        return api_response.properties

    except ApiException as e:

        data['result'] = str(e.body)
        
        # add_data_analyst(data)

        return {'message': "Exception when creating contact: %s\n" % e.body}
