from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi import APIRouter, Form, Depends, Request, Cookie, HTTPException


router = APIRouter(prefix="/gemini")

# Google API 키 설정
GOOGLE_API_KEY = "AIzaSyCHADfi0J8bptpzZOUWP_3sXyGU2kBcL7w"
genai.configure(api_key=GOOGLE_API_KEY)

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
        prompt = f"문제: {problem}\n내용: {content}\n답변: {answer}\n\n이 답변의 문법적 오류를 찾아 수정하고, 개선할 점을 알려주세요."
        response = genai.generate(
            model="gemini-1.5-flash",
            prompt=prompt,
        )
        feedback = response['generations'][0]['text']

        return {"answer": answer, "feedback": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
