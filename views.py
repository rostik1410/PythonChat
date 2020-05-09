from flask import session, redirect, url_for, render_template, request, flash, Blueprint, jsonify

view = Blueprint('views', __name__, template_folder='templates')


@view.route('/')
def index():
    if not session.get('nickname'):
        return redirect(url_for('login'))

    return render_template('chat.html')


@view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if nickname:
            session['nickname'] = nickname
            session['first_name'] = first_name
            session['last_name'] = last_name

            flash(f"You are successfully logged in as {nickname}.")
            return redirect('/')

    return render_template('login.html')


@view.route('/get_nickname')
def get_nickname():
    nickname = session.get('nickname')
    data = {'nickname': nickname}
    return jsonify(data)
