from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(String)
    created_at = Column(DateTime)
    sent = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User")
