from flask_socketio import SocketIO

from chat_app import create_app, db
from chat_app.models import Message

app = create_app()
socketio = SocketIO(app)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')


@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    data = dict(json)
    if "current_user" in data:
        message = Message(text=data.get('message'), author_id=data.get('current_user', {}).get('id'), chat_id=1)
        db.session.add(message)
        db.session.commit()

    socketio.emit('message response', json)


