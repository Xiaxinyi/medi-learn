from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse, QuestionListResponse
from app.services.question_service import QuestionService
from app.services.ai_service import AIService
from app.middleware.auth_middleware import get_current_admin

router = APIRouter()


@router.get("/")
async def list_questions(
    type: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取题目列表"""
    questions, total = QuestionService.list_questions(db, type, difficulty, search, page, page_size)
    return {
        "items": questions,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/random", response_model=list[QuestionResponse])
async def get_random_questions(
    count: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """随机抽取题目"""
    return QuestionService.get_random_questions(db, count)


@router.post("/generate")
async def generate_question_info(
    topic: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """AI生成试题（admin）"""
    try:
        result = await AIService.generate_question_info(topic)
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成失败: {str(e)}")


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    """获取题目详情"""
    question = QuestionService.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question


@router.post("/", response_model=QuestionResponse)
async def create_question(
    data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """添加题目（admin）"""
    question = QuestionService.create_question(
        db,
        content=data.content,
        type=data.type,
        difficulty=data.difficulty,
        explanation=data.explanation,
        options=[opt.model_dump() for opt in data.options],
        tags=data.tags,
        herb_ids=data.herb_ids,
    )
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """更新题目（admin）"""
    from app.models.question import Question, QuestionOption
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    update_data = data.model_dump(exclude_unset=True)
    options_data = update_data.pop("options", None)

    for key, value in update_data.items():
        setattr(question, key, value)

    if options_data:
        db.query(QuestionOption).filter(QuestionOption.question_id == question_id).delete()
        for opt in options_data:
            option = QuestionOption(
                question_id=question_id,
                option_key=opt.get("option_key") or opt.get("key"),
                content=opt["content"],
                is_correct=opt.get("is_correct", False),
                sort_order=opt.get("sort_order", 0),
            )
            db.add(option)

    db.commit()
    db.refresh(question)
    return question


@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """删除题目（admin）"""
    from app.models.question import Question
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    db.delete(question)
    db.commit()
    return {"message": "删除成功"}
