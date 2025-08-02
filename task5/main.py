from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, EmailStr
from typing import Dict, Optional


app = FastAPI(title="Simple Contact API")

# In-memory storage
contacts: Dict[str, Dict] = {}


class Contact(BaseModel):
    name: str
    phone: str
    email: EmailStr


@app.post("/contacts/", status_code=201)
def add_contact(contact: Contact):
    try:
        if contact.name in contacts:
            raise HTTPException(
                status_code=400, detail="Contact already exists")
        contacts[contact.name] = contact.model_dump()
        return {"message": "Contact added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/contacts/")
def get_contact(name: str = Query(..., description="Name of contact to search")):
    try:
        contact = contacts.get(name)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contacts/{name}")
def update_contact(
    name: str = Path(..., description="Name of the contact to update"),
    phone: Optional[str] = Query(None),
    email: Optional[EmailStr] = Query(None)
):
    try:
        if name not in contacts:
            raise HTTPException(status_code=404, detail="Contact not found")
        if phone:
            contacts[name]["phone"] = phone
        if email:
            contacts[name]["email"] = email
        return {"message": "Contact updated", "contact": contacts[name]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/contacts/{name}")
def delete_contact(name: str = Path(..., description="Name of contact to delete")):
    try:
        if name not in contacts:
            raise HTTPException(status_code=404, detail="Contact not found")
        del contacts[name]
        return {"message": f"Contact '{name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
