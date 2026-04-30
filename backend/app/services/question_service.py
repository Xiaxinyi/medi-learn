import random
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.question import Question, QuestionOption


class QuestionService:
    @staticmethod
    def list_questions(
        db: Session,
        type: Optional[str] = None,
        difficulty: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[Question], int]:
        query = db.query(Question).options(joinedload(Question.options)).filter(Question.is_system == 1)

        if type:
            query = query.filter(Question.type == type)
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
        if search:
            query = query.filter(Question.content.contains(search))

        total = db.query(Question).filter(Question.is_system == 1).count()
        questions = query.offset((page - 1) * page_size).limit(page_size).all()
        return questions, total

    @staticmethod
    def get_question(db: Session, question_id: int) -> Optional[Question]:
        return db.query(Question).filter(Question.id == question_id).first()

    @staticmethod
    def get_random_questions(db: Session, count: int = 10) -> List[Question]:
        questions = db.query(Question).filter(Question.is_system == 1).all()
        if len(questions) <= count:
            return questions
        return random.sample(questions, count)

    @staticmethod
    def create_question(db: Session, content: str, type: str, difficulty: str, explanation: str, options: List[dict], **kwargs) -> Question:
        question = Question(
            content=content,
            type=type,
            difficulty=difficulty,
            explanation=explanation,
            **kwargs
        )
        db.add(question)
        db.commit()
        db.refresh(question)

        for opt in options:
            option = QuestionOption(
                question_id=question.id,
                option_key=opt.get("option_key") or opt.get("key"),
                content=opt["content"],
                is_correct=opt.get("is_correct", False),
                sort_order=opt.get("sort_order", 0),
            )
            db.add(option)

        db.commit()
        return question

    @staticmethod
    def calculate_score(question: Question, user_answers: List[str]) -> float:
        correct = set([o.option_key for o in question.options if o.is_correct])
        user = set(user_answers)

        if question.type == "single":
            return 1.0 if user == correct else 0.0
        else:
            if not user:
                return 0.0
            if user - correct:
                return 0.0
            correct_count = len(user & correct)
            return correct_count / len(correct)
