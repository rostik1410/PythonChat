from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit
from config import SECRET_KEY
from views import view

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.register_blueprint(view)
socketio = SocketIO(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0')


@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received json: ' + str(json))

    socketio.emit('message response', json)


