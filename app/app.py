from sqlalchemy import create_engine
from schemas import Base
from flask import Flask

engine = create_engine('postgresql://austburn:pass1234@postgres', echo=True)
Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/')
def home():
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
