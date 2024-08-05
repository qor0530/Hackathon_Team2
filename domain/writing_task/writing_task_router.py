from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi.templating import Jinja2Templates
from domain.writing_task import writing_task_crud, writing_task_schema

router = APIRouter(
    prefix="/api/writing_task",
)

templates = Jinja2Templates(directory="domain/writing_task/templates")


@router.get("/update/{writing_task_id}", response_class=HTMLResponse)
def writing_task_update_html(request: Request, writing_task_id: int, db: Session = Depends(get_db)):
    writing_task = writing_task_crud.get_writing_task(
        db, writing_task_id=writing_task_id)
    if not writing_task:
        raise HTTPException(status_code=404, detail="Writing task not found")
    return templates.TemplateResponse("writing_task_update.html", {"request": request, "writing_task": writing_task}, status_code=200)


@router.put("/update/{writing_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def writing_task_update(writing_task_id: int, _writing_task_update: writing_task_schema.WritingTaskUpdate, db: Session = Depends(get_db)):
    db_writing_task = writing_task_crud.get_writing_task(db, writing_task_id)
    if not db_writing_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Writing task not found")
    writing_task_crud.update_writing_task(
        db=db, db_writing_task=db_writing_task, writing_task_update=_writing_task_update)


@router.get("/list", response_class=HTMLResponse)
def writing_task_list_html(request: Request, db: Session = Depends(get_db)):
    writing_task_list = writing_task_crud.get_writing_task_list(db)
    return templates.TemplateResponse("writing_task_list.html", {"request": request, "writing_task_list": writing_task_list})


@router.get("/detail/{writing_task_id}", response_class=HTMLResponse)
def writing_task_detail_html(request: Request, writing_task_id: int, db: Session = Depends(get_db)):
    writing_task = writing_task_crud.get_writing_task(db, writing_task_id)
    return templates.TemplateResponse("writing_task_detail.html", {"request": request, "writing_task": writing_task})


@router.get("/create", response_class=HTMLResponse)
def writing_task_create_html(request: Request):
    return templates.TemplateResponse("writing_task_create.html", {"request": request})


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def writing_task_create(_writing_task_create: writing_task_schema.WritingTaskCreate, db: Session = Depends(get_db)):
    writing_task_crud.create_writing_task(
        db=db, writing_task_create=_writing_task_create)


@router.delete("/delete/{writing_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def writing_task_delete(writing_task_id: int, db: Session = Depends(get_db)):
    db_writing_task = writing_task_crud.get_writing_task(db, writing_task_id)
    if not db_writing_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Writing task not found")
    writing_task_crud.delete_writing_task(
        db=db, db_writing_task=db_writing_task)
