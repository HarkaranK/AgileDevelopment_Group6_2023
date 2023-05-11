from myapp import create_app

app, socketio = create_app()


if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, host="0.0.0.0", port=9000)
