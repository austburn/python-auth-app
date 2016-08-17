from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from schemas import Base, User, OTP
import bcrypt
from flask import Flask, render_template, request, redirect, g

from login import login
from signup import signup

engine = create_engine('postgresql://austburn:pass1234@postgres', echo=True)
Base.metadata.create_all(engine)

app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(signup)

@app.before_request
def initialize_session():
    Session = sessionmaker(bind=engine)
    g.session = Session()

@app.after_request
def setup_db(res):
    g.session.close()
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
