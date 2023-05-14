from flask_socketio import emit, join_room
from flask import request
from myapp.utils.handler import Predict
import openai


def init_stream_socket(socketio):
    @socketio.on('connect')
    def handle_connection():
        join_room(request.sid)

    @socketio.on('participation')
    def handle_participation(data):
        participation_id = data['participation_id']
        predict = Predict("us-central1-gcp", "quizzes")
        message = predict.get_message(participation_id)

        for chunk in openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": message
            }],
            stream=True,
        ):
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                emit('message', {'data': content}, room=request.sid)

        # Indicate that streaming has ended
        emit('end_of_stream', room=request.sid)
