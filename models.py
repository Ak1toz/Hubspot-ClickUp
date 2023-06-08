from sqlalchemy import Text, Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class Apicall(Base):
    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    endpoint = Column(String(255), nullable=False)
    params = Column(JSONB)
    result = Column(Text)

    def __repr__(self):
        return f"<Apicall(id={self.id}, create_at={self.create_at})>"