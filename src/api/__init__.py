from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import get_supabase, supabase_available, get_supabase_error

router = APIRouter()


class AttendancePayload(BaseModel):
    student_email: str
    date: str
    present: bool


@router.post("/attendance/mark")
async def mark_attendance(payload: AttendancePayload):
    # Insert attendance row, rely on RLS
    if not supabase_available():
        raise HTTPException(status_code=503, detail=f"Supabase not available: {get_supabase_error()}")
    try:
        supabase = get_supabase()
        supabase.table("attendance").insert({
            "student_email": payload.student_email,
            "date": payload.date,
            "present": payload.present,
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok"}


class MarksPayload(BaseModel):
    student_email: str
    subject: str
    marks: float


@router.post("/marks/update")
async def update_marks(payload: MarksPayload):
    if not supabase_available():
        raise HTTPException(status_code=503, detail=f"Supabase not available: {get_supabase_error()}")
    try:
        supabase = get_supabase()
        supabase.table("internal_marks").insert({
            "student_email": payload.student_email,
            "subject": payload.subject,
            "marks": payload.marks,
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok"}
