from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas import Base, User
from flask import Flask, render_template, request, redirect, g

engine = create_engine('postgresql://austburn:pass1234@postgres', echo=True)
Base.metadata.create_all(engine)

app = Flask(__name__)

@app.before_request
def initialize_session():
    Session = sessionmaker(bind=engine)
    g.session = Session()

@app.after_request
def setup_db(res):
    g.session.commit()
    g.session.close()
    return res

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def login():
    g.session.add(User(email=request.form['email'], password=request.form['password']))
    return redirect('/')

@app.route('/users')
def users():
    users = g.session.query(User).all()
    return ','.join([ u.email for u in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
