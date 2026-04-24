from sqlalchemy import Column, BigInteger, String, Text, Integer, SmallInteger, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Herb(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "herbs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    latin_name = Column(String(200), nullable=True)
    aliases = Column(JSON, nullable=True)
    efficacy = Column(Text, nullable=True)
    indications = Column(Text, nullable=True)
    dosage = Column(String(200), nullable=True)
    contraindications = Column(Text, nullable=True)
    category = Column(String(50), index=True, nullable=True)
    origin = Column(String(200), nullable=True)
    is_system = Column(SmallInteger, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    images = relationship("HerbImage", back_populates="herb", cascade="all, delete-orphan")
    notes = relationship("HerbNote", back_populates="herb", cascade="all, delete-orphan")
    attribute_values = relationship("HerbAttributeValue", back_populates="herb", cascade="all, delete-orphan")


class HerbImage(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "herb_images"

    id = Column(Integer, primary_key=True)
    herb_id = Column(Integer, ForeignKey("herbs.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    sort_order = Column(Integer, default=0)
    is_cover = Column(SmallInteger, default=0)
    created_at = Column(DateTime, server_default=func.now())

    herb = relationship("Herb", back_populates="images")


class HerbNote(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "herb_notes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    herb_id = Column(Integer, ForeignKey("herbs.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    herb = relationship("Herb", back_populates="notes")


class HerbAttribute(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "herb_attributes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    group_name = Column(String(50), index=True, nullable=True)
    color = Column(String(20), nullable=True)
    is_system = Column(SmallInteger, default=1)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class HerbAttributeValue(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "herb_attribute_values"

    herb_id = Column(Integer, ForeignKey("herbs.id", ondelete="CASCADE"), primary_key=True)
    attribute_id = Column(Integer, ForeignKey("herb_attributes.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    herb = relationship("Herb", back_populates="attribute_values")
    attribute = relationship("HerbAttribute")
