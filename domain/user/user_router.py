from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import APIRouter, Depends, Request, status, HTTPException, Cookie, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi.templating import Jinja2Templates
from domain.user import user_crud, user_schema

from domain.user.user_crud import pwd_context
from starlette import status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime


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
    user_crud.exp_edit(db=db, db_user=db_user, gain_exp=gain_exp)


@router.get("/list", response_class=HTMLResponse)
def user_list_html(request: Request, db: Session = Depends(get_db)):
    user_list = user_crud.get_user_list(db)
    return templates.TemplateResponse("user_list.html", {"request": request, "user_list": user_list})


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
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user_login_id(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},
        )
    data = {
        "sub": user.login_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "login_id": user.login_id,
    }


@router.get("/logout", response_class=HTMLResponse)
def logout_html(request: Request):
    return templates.TemplateResponse("user_logout.html", {"request": request})

@router.get("/me", response_model=user_schema.User)
def read_users_me(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    # Bearer 토큰 형식에서 실제 토큰 값만 추출
    token = token.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    login_id: str = payload.get("sub")
    user = user_crud.get_user_login_id(db, login_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user