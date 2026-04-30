from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import auth, herbs, questions, exams, stats, formulas, feedback, levels, upload, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    engine.dispose()


app = FastAPI(
    title="中医学习小程序API",
    description="中医学习小程序后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(herbs.router, prefix="/api/herbs", tags=["草药"])
app.include_router(questions.router, prefix="/api/questions", tags=["题库"])
app.include_router(exams.router, prefix="/api/exams", tags=["考试"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计"])
app.include_router(formulas.router, prefix="/api/formulas", tags=["方剂"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["反馈"])
app.include_router(levels.router, prefix="/api/levels", tags=["等级"])
app.include_router(upload.router, prefix="/api/upload", tags=["上传"])
app.include_router(admin.router, prefix="/api/admin", tags=["管理员"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
