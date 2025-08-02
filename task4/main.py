from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import os

app = FastAPI(title="Notes App API")

NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)


class Note(BaseModel):
    title: str
    content: str


@app.post("/notes/", status_code=201)
def create_note(note: Note):
    filepath = os.path.join(NOTES_DIR, f"{note.title}.txt")
    try:
        if os.path.exists(filepath):
            raise HTTPException(status_code=400, detail="Note already exists")
        with open(filepath, "w") as f:
            f.write(note.content)
        return {"message": "Note created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notes/{title}")
def read_note(title: str):
    filepath = os.path.join(NOTES_DIR, f"{title}.txt")
    try:
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Note not found")
        with open(filepath, "r") as f:
            content = f.read()
        return {"title": title, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/notes/{title}")
def update_note(title: str, content: str = Body(..., embed=True)):
    filepath = os.path.join(NOTES_DIR, f"{title}.txt")
    try:
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Note not found")
        with open(filepath, "w") as f:
            f.write(content)
        return {"message": "Note updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/notes/{title}")
def delete_note(title: str):
    filepath = os.path.join(NOTES_DIR, f"{title}.txt")
    try:
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Note not found")
        os.remove(filepath)
        return {"message": "Note deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
