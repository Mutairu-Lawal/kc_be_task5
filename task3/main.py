from fastapi import FastAPI, HTTPException, Query
from typing import List
from models import JobApplication
from file_handler import load_applications, save_applications

app = FastAPI(title="Job Application Tracker API")


@app.post("/applications/", response_model=JobApplication)
def create_application(application: JobApplication):
    try:
        applications = load_applications()
        applications.append(application)
        save_applications(applications)
        return application
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/applications/", response_model=List[JobApplication])
def list_applications():
    try:
        return load_applications()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/applications/search", response_model=List[JobApplication])
def search_by_status(status: str = Query(..., example="pending")):
    try:
        applications = load_applications()
        filtered = [app for app in applications if app.status.lower()
                    == status.lower()]
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
