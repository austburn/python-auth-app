from sqlalchemy import create_engine
from schemas import Base

engine = create_engine('postgresql://austburn:pass1234@postgres', echo=True)
Base.metadata.create_all(engine)
