import os
from fastapi import APIRouter, Depends, Request, status, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi.templating import Jinja2Templates
from domain.lecture import lecture_crud, lecture_schema
from api.models import WritingTask, ComprehensionTask

router = APIRouter(
    prefix="/api/lecture",
)

templates = Jinja2Templates(directory="domain/lecture/templates")

UPLOAD_DIR = "uploads/lectures/"


@router.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"image_url": f"/{UPLOAD_DIR}{file.filename}"}


@router.get("/update/{lecture_id}", response_class=HTMLResponse)
def lecture_update_html(request: Request, lecture_id: int, db: Session = Depends(get_db)):
    lecture = lecture_crud.get_lecture(db, lecture_id=lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return templates.TemplateResponse("lecture_update.html", {"request": request, "lecture": lecture}, status_code=200)


@router.put("/update/{lecture_id}", status_code=status.HTTP_204_NO_CONTENT)
def lecture_update(lecture_id: int, _lecture_update: lecture_schema.LectureUpdate, db: Session = Depends(get_db)):
    db_lecture = lecture_crud.get_lecture(db, lecture_id)
    if not db_lecture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lecture not found")
    lecture_crud.update_lecture(
        db=db, db_lecture=db_lecture, lecture_update=_lecture_update)


@router.get("/list", response_class=HTMLResponse)
def lecture_list_html(request: Request, db: Session = Depends(get_db)):
    lecture_list = lecture_crud.get_lecture_list(db)
    return templates.TemplateResponse("lecture_list.html", {"request": request, "lecture_list": lecture_list})


@router.get("/detail/{lecture_id}", response_class=HTMLResponse)
def lecture_detail_html(request: Request, lecture_id: int, db: Session = Depends(get_db)):
    lecture = lecture_crud.get_lecture(db, lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")

    # Load related WritingTask and ComprehensionTask
    writing_tasks = db.query(WritingTask).filter(
        WritingTask.lecture_id == lecture_id).all()
    comprehension_tasks = db.query(ComprehensionTask).filter(
        ComprehensionTask.lecture_id == lecture_id).all()

    return templates.TemplateResponse("lecture_detail.html", {
        "request": request,
        "lecture": lecture,
        "writing_tasks": writing_tasks,
        "comprehension_tasks": comprehension_tasks,
    })


@router.get("/create", response_class=HTMLResponse)
def lecture_create_html(request: Request):
    return templates.TemplateResponse("lecture_create.html", {"request": request})


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def lecture_create(_lecture_create: lecture_schema.LectureCreate, db: Session = Depends(get_db)):
    lecture_crud.create_lecture(db=db, lecture_create=_lecture_create)


@router.delete("/delete/{lecture_id}", status_code=status.HTTP_204_NO_CONTENT)
def lecture_delete(lecture_id: int, db: Session = Depends(get_db)):
    db_lecture = lecture_crud.get_lecture(db, lecture_id)
    if not db_lecture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lecture not found")
    lecture_crud.delete_lecture(db=db, db_lecture=db_lecture)
