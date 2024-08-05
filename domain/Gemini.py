from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import google.generativeai as genai

router = APIRouter(prefix="/gemini")

# Google API 키 설정
GOOGLE_API_KEY = "AIzaSyCHADfi0J8bptpzZOUWP_3sXyGU2kBcL7w"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


class PromptRequest(BaseModel):
    problem: str
    content: str
    answer: str


@router.post("/grade")
async def grade_essay(request: PromptRequest):
    problem = request.problem
    content = request.content
    answer = request.answer

    try:
        # Google Generative AI를 사용한 문법 검사 및 피드백 생성
        prompt = f"문제: {problem}\n내용: {content}\n답변: {answer} 이에 대한 피드백을 작성해줘"

        # 텍스트 생성 요청 보내기
        response = model.generate_content(prompt)

        # response에서 필요한 내용을 추출하는 부분이 필요할 수 있음
        feedback = response.text
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
