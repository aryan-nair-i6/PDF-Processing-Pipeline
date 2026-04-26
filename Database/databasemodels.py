from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped
from sqlalchemy import String,Integer

class Base(DeclarativeBase):
    pass

class Jobs(Base):
 
    __tablename__="jobs"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    job_id:Mapped[str]=mapped_column(String)
    file_address:Mapped[str]=mapped_column(String)
    text:Mapped[str]=mapped_column(String,nullable=True)
    summary:Mapped[str]=mapped_column(String,nullable=True)
    collection_name:Mapped[str]=mapped_column(String,nullable=True)
    stage:Mapped[str]=mapped_column(String)
    status:Mapped[str]=mapped_column(String)