from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import json
import os

app = FastAPI()

DATA_FILE = "students.json"


class StudentIn(BaseModel):
    name: str
    subject_scores: Dict[str, float]


class StudentOut(StudentIn):
    average: float
    grade: str


def calculate_average(scores: Dict[str, float]) -> float:
    return sum(scores.values()) / len(scores)


def calculate_grade(average: float) -> str:
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def load_data() -> Dict[str, dict]:
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception:
        # If file is invalid, reinitialize as empty dict
        with open(DATA_FILE, "w") as f:
            f.write("{}")
        return {}


def save_data(data: Dict[str, dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.post("/students/", response_model=StudentOut)
def create_student(student: StudentIn):
    try:
        data = load_data()
        name = student.name.lower()

        if name in data:
            raise HTTPException(
                status_code=400, detail="Student already exists.")

        avg = round(calculate_average(student.subject_scores), 2)
        grade = calculate_grade(avg)

        student_data = {
            "name": student.name,
            "subject_scores": student.subject_scores,
            "average": avg,
            "grade": grade
        }

        data[name] = student_data
        save_data(data)
        return student_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/students/{name}", response_model=StudentOut)
def get_student(name: str):
    try:
        data = load_data()
        student = data.get(name.lower())
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/students/", response_model=List[StudentOut])
def list_students():
    try:
        data = load_data()
        return list(data.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
