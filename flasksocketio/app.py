from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('my_event')
def handle_my_custom_event(json):
    print('Received json: ' + str(json))
    emit('response', {'data': 'Got it!'})

@socketio.on('ping')
def handle_ping():
    emit('pong')

if __name__ == '__main__':

