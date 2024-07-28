from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi.templating import Jinja2Templates
from domain.comprehension_task import comprehension_task_crud, comprehension_task_schema

router = APIRouter(
    prefix="/api/comprehension_task",
)

templates = Jinja2Templates(directory="domain/comprehension_task/templates")


@router.get("/update/{comprehension_task_id}", response_class=HTMLResponse)
def comprehension_task_update_html(request: Request, comprehension_task_id: int, db: Session = Depends(get_db)):
    comprehension_task = comprehension_task_crud.get_comprehension_task(
        db, comprehension_task_id=comprehension_task_id)
    if not comprehension_task:
        raise HTTPException(
            status_code=404, detail="Comprehension task not found")
    return templates.TemplateResponse("comprehension_task_update.html", {"request": request, "comprehension_task": comprehension_task}, status_code=200)


@router.put("/update/{comprehension_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def comprehension_task_update(comprehension_task_id: int, _comprehension_task_update: comprehension_task_schema.ComprehensionTaskUpdate, db: Session = Depends(get_db)):
    db_comprehension_task = comprehension_task_crud.get_comprehension_task(
        db, comprehension_task_id)
    if not db_comprehension_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Comprehension task not found")
    comprehension_task_crud.update_comprehension_task(
        db=db, db_comprehension_task=db_comprehension_task, comprehension_task_update=_comprehension_task_update)


@router.get("/list", response_class=HTMLResponse)
def comprehension_task_list_html(request: Request, db: Session = Depends(get_db)):
    comprehension_task_list = comprehension_task_crud.get_comprehension_task_list(
        db)
    return templates.TemplateResponse("comprehension_task_list.html", {"request": request, "comprehension_task_list": comprehension_task_list})


@router.get("/detail/{comprehension_task_id}", response_class=HTMLResponse)
def comprehension_task_detail_html(request: Request, comprehension_task_id: int, db: Session = Depends(get_db)):
    comprehension_task = comprehension_task_crud.get_comprehension_task(
        db, comprehension_task_id)
    return templates.TemplateResponse("comprehension_task_detail.html", {"request": request, "comprehension_task": comprehension_task})


@router.get("/create", response_class=HTMLResponse)
def comprehension_task_create_html(request: Request):
    return templates.TemplateResponse("comprehension_task_create.html", {"request": request})


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def comprehension_task_create(_comprehension_task_create: comprehension_task_schema.ComprehensionTaskCreate, db: Session = Depends(get_db)):
    comprehension_task_crud.create_comprehension_task(
        db=db, comprehension_task_create=_comprehension_task_create)


@router.delete("/delete/{comprehension_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def comprehension_task_delete(comprehension_task_id: int, db: Session = Depends(get_db)):
    db_comprehension_task = comprehension_task_crud.get_comprehension_task(
        db, comprehension_task_id)
    if not db_comprehension_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Comprehension task not found")
    comprehension_task_crud.delete_comprehension_task(
        db=db, db_comprehension_task=db_comprehension_task)
