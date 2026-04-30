from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from app.database import get_db
from app.schemas.exam import ExamGenerateRequest, ExamStartRequest, ExamSubmitRequest, ExamResultResponse
from app.schemas.question import AnswerSubmit, AnswerResult, QuestionResponse
from app.services.question_service import QuestionService
from app.services.level_service import LevelService
from app.middleware.auth_middleware import get_current_user
from app.models.exam import AnswerRecord, ExamResult, WrongAnswer
from app.models.question import Question

router = APIRouter()


@router.post("/generate")
async def generate_exam(
    request: ExamGenerateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """智能组卷"""
    questions = QuestionService.get_random_questions(db, request.count)
    return {
        "questions": questions,
        "total": len(questions),
    }


@router.post("/start")
async def start_exam(
    request: ExamStartRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """开始考试"""
    questions = db.query(Question).filter(Question.id.in_(request.question_ids)).all()
    return {
        "exam_name": request.exam_name or "模拟考试",
        "questions": questions,
        "started_at": datetime.now(),
    }


@router.post("/submit")
async def submit_exam(
    request: ExamSubmitRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """提交试卷"""
    total_questions = len(request.answers)
    correct_count = 0
    total_score = 0.0
    max_score = 0.0
    results: List[AnswerResult] = []

    for ans in request.answers:
        question = db.query(Question).filter(Question.id == ans["question_id"]).first()
        if not question:
            continue

        score = QuestionService.calculate_score(question, ans.get("answers", []))
        is_correct = score >= 1.0
        if is_correct:
            correct_count += 1

        total_score += score
        max_score += 1.0

        # 记录答题
        record = AnswerRecord(
            user_id=current_user.id,
            question_id=question.id,
            user_answers=ans.get("answers", []),
            is_correct=1 if is_correct else 0,
            score=score,
            time_spent=ans.get("time_spent"),
        )
        db.add(record)

        correct_answers = [o.option_key for o in question.options if o.is_correct]
        results.append(AnswerResult(
            question_id=question.id,
            is_correct=is_correct,
            score=score,
            correct_answers=correct_answers,
            user_answers=ans.get("answers", []),
            explanation=question.explanation,
        ))

        # 错题本处理
        if not is_correct:
            wrong = db.query(WrongAnswer).filter(
                WrongAnswer.user_id == current_user.id,
                WrongAnswer.question_id == question.id,
            ).first()
            if wrong:
                wrong.wrong_count += 1
                wrong.last_wrong_at = datetime.now()
                wrong.is_mastered = 0
            else:
                wrong = WrongAnswer(
                    user_id=current_user.id,
                    question_id=question.id,
                    user_answers=ans.get("answers", []),
                    correct_answers=correct_answers,
                )
                db.add(wrong)
        else:
            # 答对了，检查是否在错题本中
            wrong = db.query(WrongAnswer).filter(
                WrongAnswer.user_id == current_user.id,
                WrongAnswer.question_id == question.id,
                WrongAnswer.is_mastered == 0,
            ).first()
            if wrong:
                # 连续答对可标记为已掌握（简化：单次答对不自动标记）
                pass

    # 保存考试结果
    exam_result = ExamResult(
        user_id=current_user.id,
        exam_name="模拟考试",
        total_questions=total_questions,
        correct_count=correct_count,
        score=round(total_score, 2),
        max_score=round(max_score, 2),
    )
    db.add(exam_result)

    # 增加经验值
    exp_type = "exam_complete"
    LevelService.add_experience(db, current_user, exp_type, f"完成考试，得分 {round(total_score, 2)}")

    # 答题经验
    for ans in request.answers:
        question = db.query(Question).filter(Question.id == ans["question_id"]).first()
        if question:
            score = QuestionService.calculate_score(question, ans.get("answers", []))
            if score >= 1.0:
                LevelService.add_experience(db, current_user, "answer_correct", f"答对题目 #{question.id}")
            else:
                LevelService.add_experience(db, current_user, "answer_wrong", f"答错题目 #{question.id}")

    db.commit()
    db.refresh(exam_result)

    return {
        "result": exam_result,
        "details": results,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "score": round(total_score, 2),
        "max_score": round(max_score, 2),
    }


@router.get("/results")
async def list_exam_results(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取考试成绩列表"""
    results = db.query(ExamResult).filter(ExamResult.user_id == current_user.id).order_by(ExamResult.completed_at.desc()).all()
    return results


@router.get("/results/{result_id}")
async def get_exam_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取成绩详情"""
    result = db.query(ExamResult).filter(ExamResult.id == result_id, ExamResult.user_id == current_user.id).first()
    if not result:
        raise HTTPException(status_code=404, detail="成绩不存在")
    return result


@router.get("/practice", response_model=list[QuestionResponse])
async def get_practice_questions(
    count: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取练习题目：优先未做过的题，不足则从错题本补足"""
    import random

    # 1. 获取用户已做过的题目ID
    answered_ids = db.query(AnswerRecord.question_id).filter(
        AnswerRecord.user_id == current_user.id
    ).distinct().all()
    answered_ids = {r[0] for r in answered_ids}

    # 2. 获取未做过的系统题目
    query = db.query(Question).options(joinedload(Question.options)).filter(Question.is_system == 1)
    if answered_ids:
        query = query.filter(~Question.id.in_(answered_ids))

    unanswered = query.all()
    if len(unanswered) > count:
        unanswered = random.sample(unanswered, count)

    result = list(unanswered)
    remaining = count - len(result)

    # 3. 不足则从错题本（未掌握）按 wrong_count 降序补足
    if remaining > 0:
        wrong_entries = db.query(WrongAnswer).filter(
            WrongAnswer.user_id == current_user.id,
            WrongAnswer.is_mastered == 0,
        ).order_by(WrongAnswer.wrong_count.desc()).all()

        existing_ids = {q.id for q in result}
        seen = set()
        additional_qids = []
        for w in wrong_entries:
            if w.question_id not in seen and w.question_id not in existing_ids:
                seen.add(w.question_id)
                additional_qids.append(w.question_id)
                if len(additional_qids) >= remaining:
                    break

        if additional_qids:
            additional = db.query(Question).options(joinedload(Question.options)).filter(
                Question.id.in_(additional_qids)
            ).all()
            result.extend(additional)

    return result


@router.get("/wrongbook")
async def list_wrong_answers(
    is_mastered: int = 0,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取错题本"""
    query = db.query(WrongAnswer).filter(
        WrongAnswer.user_id == current_user.id,
        WrongAnswer.is_mastered == is_mastered,
    )
    items = query.order_by(WrongAnswer.last_wrong_at.desc()).all()
    return items


@router.post("/wrongbook/{question_id}/master")
async def master_wrong_answer(
    question_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """标记错题已掌握"""
    wrong = db.query(WrongAnswer).filter(
        WrongAnswer.user_id == current_user.id,
        WrongAnswer.question_id == question_id,
    ).first()
    if not wrong:
        raise HTTPException(status_code=404, detail="错题记录不存在")
    wrong.is_mastered = 1
    wrong.mastered_at = datetime.now()
    db.commit()

    # 增加经验值
    LevelService.add_experience(db, current_user, "wrongbook_review", f"掌握错题 #{question_id}")

    return {"message": "已标记为掌握"}
