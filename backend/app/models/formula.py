from sqlalchemy import Column, BigInteger, String, Text, Integer, SmallInteger, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Formula(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False, index=True)
    source = Column(String(200), nullable=True)
    category = Column(String(50), index=True, nullable=True)
    indications = Column(Text, nullable=True)
    usage = Column(Text, nullable=True)
    modifications = Column(Text, nullable=True)
    precautions = Column(Text, nullable=True)
    is_system = Column(SmallInteger, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    formula_herbs = relationship("FormulaHerb", back_populates="formula", cascade="all, delete-orphan")


class FormulaHerb(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "formula_herbs"

    id = Column(Integer, primary_key=True)
    formula_id = Column(Integer, ForeignKey("formulas.id", ondelete="CASCADE"), nullable=False, index=True)
    herb_id = Column(Integer, ForeignKey("herbs.id"), nullable=False, index=True)
    herb_name = Column(String(100), nullable=True)
    dosage = Column(String(50), nullable=True)
    role = Column(Enum('chief', 'deputy', 'assistant', 'envoy'), default='assistant')
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    formula = relationship("Formula", back_populates="formula_herbs")
