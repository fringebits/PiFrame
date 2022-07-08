import bottle
import logging

# Python 3 server example
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time
import threading
#from .frame import Frame

#host = "localhost"
host = '0.0.0.0'
port = 8080
frame = None

app = bottle.Bottle()

@app.route('/')
def index():
    logging.debug(f"server.route(index):  Frame={frame}, Host={host}, Port={port}")
    photo = frame.GetCurrentPhoto()
    return f'''
        Image {frame.GetCurrentIndex()} of {frame.GetNumPhotos()} <br>
        IsPaused = {frame.IsPaused()} <br>
        Photo = {photo} <br>
        Title = {photo.fullpath} <br>
        <a href="/next">Next</a> <br>
        <a href="/pause">Pause</a> <br>
        <a href="/prev">Previous</a> <br>
    '''
        # <a href="http://{host}:{port}/next">Next</a> <br>
        # <a href="http://{host}:{port}/pause">Pause</a> <br>
        # <a href="http://{host}:{port}/prev">Previous</a> <br>

@app.route('/pause')
def pause():
    logging.debug(f"server.route(pause):  Frame={frame}, Host={host}, Port={port}")
    frame.SetIsPaused(not frame.IsPaused())
    bottle.redirect('/')

@app.route('/next')
def pause():
    logging.debug(f"server.route(next):  Frame={frame}, Host={host}, Port={port}")
    frame.NextImage(+1)
    frame.SetIsPaused(True)
    bottle.redirect('/')

@app.route('/prev')
def pause():
    logging.debug(f"server.route(prev):  Frame={frame}, Host={host}, Port={port}")
    frame.NextImage(-1)
    frame.SetIsPaused(True)
    bottle.redirect('/')

def Run(_frame, _isdebug):
    global frame
    global host
    global port
    frame = _frame

    logging.debug(f"server.Run({frame}): NumPhotos={frame.GetNumPhotos()}")

    if _isdebug:
        host = 'localhost'

    threading.Thread(
        daemon = True,
        target = bottle.run,
        kwargs = dict(app=app, host=host, port=port)).start()