from flask_socketio import emit
from myapp.utils.handler import Predict
import openai


def init_stream_socket(socketio):
    @socketio.on('connect')
    def handle_connection():
        predict = Predict("us-central1-gcp", "quizzes")
        message = predict.get_message(1)

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
                emit('message', {'data': content})