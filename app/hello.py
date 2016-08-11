from sqlalchemy import create_engine

engine = create_engine('postgresql://austburn:pass1234@postgres')

print engine.name
