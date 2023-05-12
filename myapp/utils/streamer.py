from flask_socketio import emit
from myapp.utils.handler import Predict
import openai


def init_stream_socket(socketio):
    @socketio.on('connect')
    async def handle_connection():
        predict = Predict("us-central1-gcp", "quizzes")
        message = predict.get_message(1)

        for chunk in await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": message
            }],
            stream=True,
        ):
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                await emit('message', {'data': content})
