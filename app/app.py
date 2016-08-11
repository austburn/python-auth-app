from sqlalchemy import create_engine
from schemas import Base
from flask import Flask, render_template, request, redirect

engine = create_engine('postgresql://austburn:pass1234@postgres', echo=True)
Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def login():
    print(request.form)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
