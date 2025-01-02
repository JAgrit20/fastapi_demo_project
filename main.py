from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
from threading import Thread
import json
from datetime import datetime
from sqlalchemy.orm import Session  # Replace with your ORM if different

app = FastAPI()

VERIFY_TOKEN = "2d790a4d-7c9c-4e23-9c9c-5749c5fa7fdb"

def get_time():
    return datetime.now()

def get_seconds():
    return int(datetime.now().timestamp())

def process_data(data):
    # Define your data processing logic here
    pass

@app.get("/whatsapp-webhook")
def whatsapp_webhook_get(hub_mode: Optional[str] = None, hub_verify_token: Optional[str] = None, hub_challenge: Optional[str] = None):
    dtobj_indiaa = get_time()
    time_in_sec1 = get_seconds()

    print("\nNew incoming GET request at", dtobj_indiaa)

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    else:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/whatsapp-webhook")
async def whatsapp_webhook_post(request: Request):
    dtobj_indiaa = get_time()
    time_in_sec1 = get_seconds()

    print("\nNew incoming POST request at", dtobj_indiaa)

    try:
        data = await request.json()
        
        if 'statuses' in data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}):
            pass
        else:
            if data.get('object') == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        message_type = entry['changes'][0]['value']['messages'][0]['type']
                        whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        
                        # Replace this with your ORM create/save logic
                        add_data = WhatsappDataKPI(
                            time=dtobj_indiaa,
                            mobile_number=whatsAppId,
                            response_from_user=message_type,
                            response_from_us=""
                        )
                        
                        # Simulate ORM session
                        session = Session()  # Replace with your session initialization
                        session.add(add_data)
                        session.commit()
                        session.close()

                except Exception as e:
                    print("Error in adding KPI:", e)

        print("\ndata", data)
        
        # Start a new thread for processing the data
        t = Thread(target=process_data, args=(data,))
        t.start()

        return {"status": "success"}

    except Exception as e:
        print("Error in processing request:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ORM model simulation (replace with your ORM model)
class WhatsappDataKPI(BaseModel):
    time: datetime
    mobile_number: str
    response_from_user: str
    response_from_us: str
