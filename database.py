from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database
DATABASE_URL = "sqlite:///analysis.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Analysis(Base):
    __tablename__ = "analysis"

    task_id = Column(String, primary_key=True, index=True)
    status = Column(String)
    file_name = Column(String)
    query = Column(Text)
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)


# Create tables automatically
Base.metadata.create_all(bind=engine)