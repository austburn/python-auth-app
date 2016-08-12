from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from schemas import Base, User
import bcrypt
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
    g.session.close()
    return res

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def login():
    user = g.session.query(User).filter(User.email==request.form['email']).one()
    if bcrypt.checkpw(bytes(request.form['password']), bytes(user.password)):
        return redirect('/success')
    return redirect('/')

@app.route('/success', methods=['GET'])
def success():
    return 'you successfully logged in'

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def make_account():
    hashed_pwd = bcrypt.hashpw(bytes(request.form['password']), bcrypt.gensalt())
    g.session.add(User(name=request.form['name'], email=request.form['email'], password=hashed_pwd))
    try:
        g.session.commit()
    except IntegrityError:
        return render_template('signup.html', errors=['Looks like that email is taken.'])
    return redirect('/')

@app.route('/users')
def users():
    users = g.session.query(User).all()
    return ','.join([ u.email for u in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
