"""
Database configuration và models cho hệ thống training phát âm tiếng Anh
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/military_english")

# SQLAlchemy setup
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Test connections trước khi sử dụng
    pool_size=20,        # Cho 100 users
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """Model cho user"""
    __tablename__ = "users"
    
    user_id = Column(String(50), primary_key=True, index=True)
    username = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("TrainingSession", back_populates="user", cascade="all, delete-orphan")
    stats = relationship("UserStats", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email})>"


class TrainingSession(Base):
    """Model cho mỗi session training"""
    __tablename__ = "training_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.user_id"), index=True)
    unit = Column(Integer)  # Unit 1, 2, 3, 4, hoặc 0 (General)
    level = Column(String(20))  # word, phrase, sentence
    item_count = Column(Integer)  # Số item trong session (10, 20, 30...)
    total_items = Column(Integer)  # Tổng số items
    
    # Kết quả
    excellent = Column(Integer, default=0)  # ≥95%
    good = Column(Integer, default=0)       # 85-94%
    fair = Column(Integer, default=0)       # 70-84%
    poor = Column(Integer, default=0)       # <70%
    
    average_score = Column(Float, default=0.0)
    details = Column(JSON, nullable=True)  # Chi tiết mỗi item: {"hello": 92.5, "hi": 88.0}
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    duration_seconds = Column(Integer, nullable=True)  # Thời gian training (giây)
    
    # Relationship
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<TrainingSession(user_id={self.user_id}, unit={self.unit}, level={self.level}, avg={self.average_score})>"


class UserStats(Base):
    """Model cho thống kê tổng hợp của user"""
    __tablename__ = "user_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.user_id"), unique=True, index=True)
    
    # Thống kê tổng cộng
    total_sessions = Column(Integer, default=0)
    total_training_seconds = Column(Integer, default=0)
    
    # Per-level stats (unit-agnostic)
    word_excellent = Column(Integer, default=0)
    word_good = Column(Integer, default=0)
    word_fair = Column(Integer, default=0)
    word_poor = Column(Integer, default=0)
    word_avg_score = Column(Float, default=0.0)
    
    phrase_excellent = Column(Integer, default=0)
    phrase_good = Column(Integer, default=0)
    phrase_fair = Column(Integer, default=0)
    phrase_poor = Column(Integer, default=0)
    phrase_avg_score = Column(Float, default=0.0)
    
    sentence_excellent = Column(Integer, default=0)
    sentence_good = Column(Integer, default=0)
    sentence_fair = Column(Integer, default=0)
    sentence_poor = Column(Integer, default=0)
    sentence_avg_score = Column(Float, default=0.0)
    
    # Unit-specific stats (JSON for flexibility)
    unit_progress = Column(JSON, default={})  # {"1": {"word": 80, "phrase": 75}, "2": {...}}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="stats")
    
    def __repr__(self):
        return f"<UserStats(user_id={self.user_id}, sessions={self.total_sessions})>"


def init_db():
    """Tạo tất cả tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def get_db():
    """Dependency injection cho Flask routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test connection
if __name__ == "__main__":
    try:
        init_db()
        print("✅ PostgreSQL connection successful")
        
        # Test insert
        db = SessionLocal()
        user = User(user_id="test_user", email="test@example.com")
        db.add(user)
        db.commit()
        print("✅ Test user created")
        db.close()
    except Exception as e:
        print(f"❌ Error: {e}")
