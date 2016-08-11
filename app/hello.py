from sqlalchemy import create_engine

engine = create_engine('postgresql://austburn:pass1234@postgres', echo=True)
connection = engine.connect()

print connection.info

connection.close()
