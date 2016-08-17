from flask import Blueprint, render_template, redirect, g


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
        return redirect('/success')
    return err_response

@login.route('/success', methods=['GET'])
def success():
    return 'you successfully logged in'
