from flask_socketio import emit, join_room
from flask import request
from myapp.utils.handler import Predict
import openai


def init_stream_socket(socketio):
    """
    Initializes the socketio server and registers the event handlers.

    Args:
        socketio (SocketIO): The flask_socketio instance.
    """
    @socketio.on('connect')
    def handle_connection():
        """
        Handles new client connections and adds the client to a new socket.io room.
        """
        join_room(request.sid)

    @socketio.on('participation')
    def handle_participation(data):
        """
        Handles the 'participation' event and emits chat completion results back to the client.

        Args:
            data (dict): The event data. It's expected to have a 'participation_id' key with the ID of the quiz participation as the value.
        """
        participation_id = data['participation_id']
        predict = Predict("us-central1-gcp", "quizzes")
        message = predict.get_message(participation_id)

        for chunk in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
