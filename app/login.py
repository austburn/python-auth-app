from flask import Blueprint, render_template, redirect, g, session, request
import bcrypt

from schemas import User, OTP


login = Blueprint('login', __name__, template_folder='templates')

@login.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@login.route('/', methods=['POST'])
def login_action():
    err_response = render_template('home.html', errors=['Looks like the email or password were incorrect.'])
    try:
        user = g.session.query(User).filter(User.email==request.form['email']).one()
    except Exception:
        return err_response

    if bcrypt.checkpw(bytes(request.form['password']), bytes(user.password)):
        session['email'] = user.email
        session['confirmed'] = user.confirmed
        return redirect('/success')
    return err_response

@login.route('/success', methods=['GET'])
def success():
    return 'you successfully logged in as {}, this email is {}confirmed'.format(session['email'], 'not ' if not session['confirmed'] else '')
