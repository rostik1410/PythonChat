from flask import session, redirect, url_for, render_template, request, flash, Blueprint, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from chat_app import db
from chat_app.models import User, Message

view = Blueprint('views', __name__, template_folder='templates')


@view.route('/')
@login_required
def index():
    messages = Message.query.filter_by(chat_id=1).all()
    return render_template('index.html', messages=messages, current_user=current_user)


@view.route('/login')
def login():
    return render_template('login.html')


@view.route('/login', methods=['POST'])
def login_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user = User.query.filter_by(nickname=nickname).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('views.login'))

    login_user(user)
    return redirect(url_for('views.index'))


@view.route('/signup')
def signup():
    return render_template('signup.html')


@view.route('/signup', methods=['POST'])
def signup_post():
    nickname = request.form.get('nickname')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    user = User.query.filter_by(
        nickname=nickname).first()  # if this returns a user, then the nickname already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash("That nickname is already exist. Please try another or login with exist.")
        return redirect(url_for('views.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(nickname=nickname, first_name=first_name, last_name=last_name,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('views.login'))


@view.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@view.route('/get_current_user')
@login_required
def get_current_user():
    data = {
        'id': current_user.id,
        'nickname': current_user.nickname,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
    }
    return jsonify(data)
