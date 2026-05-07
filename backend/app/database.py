import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# TiDB Serverless 公共端点需要 TLS 连接
connect_args = {}
if "tidbcloud.com" in settings.DATABASE_URL:
    # 尝试多个常见的 CA 证书路径（macOS / Debian / Alpine）
    ca_paths = [
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
    ]
    ca_file = next((p for p in ca_paths if os.path.exists(p)), None)
    if ca_file:
        connect_args["ssl"] = {"ca": ca_file}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
