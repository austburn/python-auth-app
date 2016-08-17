from flask import Blueprint, render_template, redirect, g


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

    g.session.add(OTP(new_user.id))
    g.session.commit()
    return redirect('/')

@signup.route('/users')
def users():
    users = g.session.query(User).all()
    return ','.join([ u.email for u in users])
