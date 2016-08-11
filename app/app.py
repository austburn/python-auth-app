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
    users = g.session.query(User).filter(User.email==request.form['email'], User.password==request.form['password']).count()
    if users:
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
    g.session.add(User(name=request.form['name'], email=request.form['email'], password=request.form['password']))
    return redirect('/')

@app.route('/users')
def users():
    users = g.session.query(User).all()
    return ','.join([ u.email for u in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
