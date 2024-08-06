from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from config.database import get_db
from domain.quiz import quiz_crud, quiz_schema
from api.models import User, Quiz
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql.expression import func
router = APIRouter(
    prefix="/api/quiz",
)

templates = Jinja2Templates(directory="domain/quiz/templates")


@router.get("/update/{quiz_id}", response_class=HTMLResponse)
def quiz_update_html(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    quiz = quiz_crud.get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        print("quiz not found")
        raise HTTPException(status_code=404, detail="Quiz not found")
    return templates.TemplateResponse("quiz_update.html", {"request": request, "quiz": quiz}, status_code=200)


@router.patch("/update/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def quiz_update(quiz_id: int, _quiz_update: quiz_schema.QuizUpdate, db: Session = Depends(get_db)):
    db_quiz = quiz_crud.get_quiz(db, quiz_id)
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz not found")
    quiz_crud.update_quiz(db=db, db_quiz=db_quiz, quiz_update=_quiz_update)


@router.get("/list", response_class=HTMLResponse)
def quiz_list_html(request: Request, db: Session = Depends(get_db)):
    quiz_list = quiz_crud.get_quiz_list(db)
    return templates.TemplateResponse("quiz_list.html", {"request": request, "quiz_list": quiz_list})


@router.get("/detail/{quiz_id}", response_class=HTMLResponse)
def quiz_detail_html(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    quiz = quiz_crud.get_quiz(db, quiz_id)
    return JSONResponse(content=quiz)


@router.get("/create", response_class=HTMLResponse)
def quiz_create_html(request: Request):
    return templates.TemplateResponse("quiz_create.html", {"request": request})


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def quiz_create(_quiz_create: quiz_schema.QuizCreate, db: Session = Depends(get_db)):
    quiz_crud.create_quiz(db=db, quiz_create=_quiz_create)


@router.delete("/delete/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def quiz_delete(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = quiz_crud.get_quiz(db, quiz_id)
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz not found")
    quiz_crud.delete_quiz(db=db, db_quiz=db_quiz)


@router.get("/quizzes/{quiz_type}")
def get_quizzes(quiz_type: str, user_id: int, db: Session = Depends(get_db)):
    quizzes = quiz_crud.get_quizzes_by_type(db, user_id, quiz_type)
    if not quizzes:
        raise HTTPException(
            status_code=404, detail="No quizzes found for this type")
    return quizzes


@router.post("/update_quiz_stack")
def update_quiz_stack(user_id: int, quiz_stack: list[int], db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.quiz_stack = str(quiz_stack)  # JSON 형식으로 저장
    db.commit()
    return {"success": True}


@router.get("/next_quiz/{user_id}")
def next_quiz(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # user.quiz_stack을 str에서 list로 변환
    quiz_stack = user.quiz_stack.split(',')
    quiz_stack = [int(q) for q in quiz_stack if q]

    if not quiz_stack:
        return JSONResponse(content={"error": "quiz_stack_empty"}, status_code=200)

    # 첫 번째 퀴즈 ID를 pop하여 next_quiz_id에 저장
    next_quiz_id = quiz_stack.pop(0)

    # 변환된 quiz_stack을 다시 문자열로 저장
    user.quiz_stack = ','.join(map(str, quiz_stack))
    db.commit()

    # /quiz/{next_quiz_id}로 리다이렉트
    return RedirectResponse(url=f"/quiz/{next_quiz_id}")


@router.get("/start_quiz/{quiz_type}")
def start_quiz(quiz_type: str, user_id: int, db: Session = Depends(get_db)):
    quizzes = quiz_crud.get_quizzes_by_type(db, user_id, quiz_type)
    if not quizzes:
        if quiz_type == "incorrect":
            return JSONResponse(content={"error": "no_incorrect_quizzes"}, status_code=200)
        if quiz_type == "level":
            return JSONResponse(content={"error": "no_level_quizzes"}, status_code=200)
        if quiz_type == "random":
            return JSONResponse(content={"error": "no_random_quizzes"}, status_code=200)
        return JSONResponse(content={"error": "no_quizzes_found"}, status_code=200)

    quiz_stack = [quiz.id for quiz in quizzes]
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.quiz_stack = str(quiz_stack)  # JSON 형식으로 저장
    db.commit()

    if quiz_stack:
        next_quiz_id = quiz_stack[0]
        return RedirectResponse(url=f"/quiz/{next_quiz_id}")
    else:
        return JSONResponse(content={"error": "quiz_stack_empty"}, status_code=200)


@router.get("/next_quiz/{user_id}")
def next_quiz(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # user.quiz_stack을 str에서 list로 변환
    quiz_stack = user.quiz_stack.split(',')

    if not quiz_stack:
        raise HTTPException(status_code=404, detail="No quizzes available")

    # 첫 번째 퀴즈 ID를 pop하여 next_quiz_id에 저장
    next_quiz_id = quiz_stack.pop(0)

    # 변환된 quiz_stack을 다시 문자열로 저장
    user.quiz_stack = ','.join(quiz_stack)
    db.add(user)
    db.commit()
    # /quiz/{next_quiz_id}로 리다이렉트
    return RedirectResponse(url=f"/quiz/{next_quiz_id}")


@ router.get("/{quiz_id}", response_class=HTMLResponse)
def quiz_html(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    quiz = quiz_crud.get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return templates.TemplateResponse("quiz.html", {"request": request, "quiz": quiz}, status_code=200)


@router.get("/random_quizzes/{user_id}")
def random_quizzes(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # db에서 Quiz 중 랜덤으로 10개 가져오기
    quiz_stack = db.query(Quiz).order_by(func.random()).limit(10).all()

    quiz_stack = [quiz.id for quiz in quiz_stack]
    user.quiz_stack = ','.join(map(str, quiz_stack))
    db.commit()
    return quiz_stack


@router.get("/similar_level_quizzes/{user_id}")
def get_similar_level_quizzes(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 유저의 레벨을 기준으로 비슷한 레벨의 퀴즈를 가져옴
    user_level = user.level  # 유저의 레벨 정보가 있다고 가정
    similar_level_quizzes = db.query(Quiz).filter(
        Quiz.level >= user_level - 2,
        Quiz.level <= user_level + 2
    ).all()

    if not similar_level_quizzes:
        raise HTTPException(
            status_code=404, detail="No similar level quizzes found")

    quiz_stack = [quiz.id for quiz in similar_level_quizzes]
    user.quiz_stack = ','.join(map(str, quiz_stack))
    db.commit()

    return {"quiz_stack": quiz_stack}
