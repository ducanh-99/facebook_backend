from main import app, socketio
  

if __name__ == "__main__": 
    app.debug = True
    socketio.run(app)
    # app.run(debug=True)