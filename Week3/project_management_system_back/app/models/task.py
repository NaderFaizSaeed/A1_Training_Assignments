from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="TODO")

    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User", back_populates="tasks")