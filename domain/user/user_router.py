from api.models import User
import logging
from api.models import User, Lecture
from typing import List
from passlib.context import CryptContext
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status
from domain.user.user_crud import pwd_context
from domain.user.user_schema import LectureResponse
from domain.user.user_crud import pwd_context, get_user_by_id, get_lectures_by_ids, get_topic_counts, get_most_frequent_topic, get_lectures_by_topic, parse_learning_history
from fastapi import APIRouter, Depends, status, HTTPException, Cookie, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi.templating import Jinja2Templates
from domain.user import user_crud, user_schema
<< << << < HEAD
== == == =
>>>>>> > main
<< << << < HEAD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

== == == =
>>>>>> > main
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "0db75ab2ce9e9f2ebe7f231f01fdcb11bd94219f5c71194b537c70bf6d80a8f3"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/api/user",
)

templates = Jinja2Templates(directory="domain/user/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
active_sessions = set()


@router.get("/update/{user_id}", response_class=HTMLResponse)  # user_id로 수정
def user_update_html(request: Request, user_id: int, db: Session = Depends(get_db)):  # user_id로 수정
    user = user_crud.get_user(db, user_id=user_id)  # user_id로 수정
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_update.html", {"request": request, "user": user}, status_code=200)


# user_id로 수정
@router.patch("/update/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def user_update(user_id: int, gain_exp: int, db: Session = Depends(get_db)):  # user_id로 수정
    db_user = user_crud.get_user(db, user_id=user_id)  # user_id로 수정
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    user_crud.exp_edit(db=db, db_user=db_user, change_exp=gain_exp)


@router.get("/list", response_class=HTMLResponse)
def user_list_html(request: Request, db: Session = Depends(get_db)):
    user_list = user_crud.get_user_list(db)
    return templates.TemplateResponse("user_list.html", {"request": request, "user_list": user_list})


@router.get("/login_ids", response_model=List[str])
def get_login_ids(db: Session = Depends(get_db)):
    login_ids = user_crud.get_login_ids(db)
    return [str(login_id[0]) for login_id in login_ids]


@router.get("/detail/{user_id}", response_class=HTMLResponse)  # user_id로 수정
def user_detail_html(request: Request, user_id: int, db: Session = Depends(get_db)):  # user_id로 수정
    user = user_crud.get_user(db, user_id=user_id)  # user_id로 수정
    if not user:
        print(user.id)
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})


@router.get("/create", response_class=HTMLResponse)
def user_create_html(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)


# user_id로 수정
@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(user_id: int, db: Session = Depends(get_db)):  # user_id로 수정
    db_user = user_crud.get_user(db, user_id=user_id)  # user_id로 수정
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    user_crud.delete_user(db=db, db_user=db_user)

# 로그인


@router.get("/login", response_class=HTMLResponse)
def login_html(request: Request):
    return templates.TemplateResponse("user_login.html", {"request": request})


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user_login_id(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {
        "sub": user.login_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=False)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "login_id": user.login_id,
    }


@router.get("/logout", response_class=HTMLResponse)
def logout_html(request: Request, response: Response):
    response.delete_cookie(key="access_token")
    return None


@router.get("/me", response_model=user_schema.User)
def read_users_me(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization cookie missing",
        )

    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login_id: str = payload.get("sub")
        if login_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = user_crud.get_user_login_id(db, login_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.get("/me/statistics")
def read_user_statistics(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization cookie missing",
        )

    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login_id: str = payload.get("sub")
        if login_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = user_crud.get_user_login_id(db, login_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "total_learning_time": user.total_learning_time,
        # assuming quiz_learning_history is a comma-separated string
        "quiz_solved": len(user.quiz_learning_history.split(',')),
        "attendance_days": user.attendance
    }


#####################
## voca 관련 라우터 ##
#####################


@router.get("/voca/list/{user_id}", response_class=JSONResponse)
def fetch_voca_list(request: Request, user_id: int, db: Session = Depends(get_db)):
    voca_list = user_crud.get_voca_list(db, user_id)
    return voca_list


@router.post("/voca/add_quiz/{user_id}/{quiz_id}", response_class=JSONResponse)
def add_quiz_to_voca(user_id: int, quiz_id: int, db: Session = Depends(get_db)):
    return user_crud.add_quiz_to_user_voca(db, user_id, quiz_id)


@router.delete("/voca/delete/{user_id}/{quiz_id}", response_class=JSONResponse)
def delete_quiz(user_id: int, quiz_id: int, db: Session = Depends(get_db)):
    return user_crud.delete_quiz_from_user_voca(db, user_id, quiz_id)


@router.get("/most_frequent_topic/{user_id}", response_model=List[LectureResponse])
def get_most_frequent_topic(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Parse lecture_learning_history to get a list of IDs
    learning_history = user.lecture_learning_history
    lecture_ids = parse_learning_history(learning_history)

    # Get lectures by IDs and count the frequency of each topic
    lectures = get_lectures_by_ids(db, lecture_ids)
    topic_count = get_topic_counts(lectures)

    most_frequent_topic = get_most_frequent_topic(topic_count)

    if not most_frequent_topic:
        raise HTTPException(
            status_code=404, detail="No lectures found in learning history")

    # Get lectures for the most frequent topic that are not in learning history
    lectures_to_return = get_lectures_by_topic(
        db, most_frequent_topic, lecture_ids)

    return lectures_to_return
