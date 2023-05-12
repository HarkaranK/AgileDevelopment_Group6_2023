from flask_socketio import emit


def init_stream_socket(socketio):
    @socketio.on('connect', namespace='/chat')
    def handle_connect():
        emit('response', {'data': 'Connected'})

    # @socketio.on('message', namespace='/chat')
    # def handle_message(message):
    #     global vectorstore
    #     question_handler = QuestionGenCallbackHandler(socketio)
    #     stream_handler = StreamingLLMCallbackHandler(socketio)
    #     chat_history = []
    #     qa_chain = get_chain(vectorstore, question_handler, stream_handler)

    #     try:
    #         resp = ChatResponse(sender="you", message=message, type="stream")
    #         emit('response', resp.dict())

    #         start_resp = ChatResponse(sender="bot", message="", type="start")
    #         emit('response', start_resp.dict())

    #         result = qa_chain.acall(
    #             {"question": message, "chat_history": chat_history})
    #         chat_history.append((message, result["answer"]))

    #         end_resp = ChatResponse(sender="bot", message="", type="end")
    #         emit('response', end_resp.dict())
    #     except Exception as e:
    #         logging.error(e)
    #         resp = ChatResponse(
    #             sender="bot",
    #             message="Sorry, something went wrong. Try again.",
    #             type="error",
    #         )
    #         emit('response', resp.dict())

    @socketio.on('disconnect', namespace='/chat')
    def handle_disconnect():
        print('Client disconnected')
