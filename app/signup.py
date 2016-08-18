from flask import Blueprint, render_template, redirect, g, session, request
import bcrypt

from schemas import User, OTP


signup = Blueprint('signup', __name__, template_folder='templates')

@signup.route('/signup', methods=['GET'])
def signup_action():
    return render_template('signup.html')

@signup.route('/signup', methods=['POST'])
def make_account():
    hashed_pwd = bcrypt.hashpw(bytes(request.form['password']), bcrypt.gensalt())
    new_user = User(name=request.form['name'], email=request.form['email'], password=hashed_pwd)
    g.session.add(new_user)
    try:
        g.session.commit()
    except IntegrityError:
        return render_template('signup.html', errors=['Looks like that email is taken.'])

    session['email'] = request.form['email']
    g.session.add(OTP(new_user.id))
    g.session.commit()
    return redirect('/')

@signup.route('/confirm')
def confirm_email():
    key = request.args.get('key')
    user = g.session.query(User).filter(User.email==session['email']).one()
    otp = g.session.query(OTP).filter(OTP.id==user.id).one()
    if key == otp.key:
        user.confirmed = True
        g.session.commit()
        return 'Successfully confirmed email'
    return 'Nope'

@signup.route('/users')
def users():
    users = g.session.query(User).all()
    return ','.join([ u.email for u in users])
