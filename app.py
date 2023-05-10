from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb       
import math
import time
import configparser as ConfigParser
import random
import os
import serial

async_mode = None
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 

#  "a" - Append - will append to the end of the file
#  "w" - Write - will overwrite any existing content
#  "r" - Read - will read the content of the file
# pri zapise do suboru musia byt na nadradenom adresari nastavene prava na zapis do adresaru

@app.route('/write')
def write2file():
    fo = open("static/files/test.txt","a+")    
    val = '[{"y": 0.6551787400492523, "x": 1, "t": 1522016547.531831}, {"y": 0.47491473008127605, "x": 2, "t": 1522016549.534749}, {"y": 0.7495528524284468, "x": 3, "t": 1522016551.537547}, {"y": 0.19625207463282368, "x": 4, "t": 1522016553.540447}, {"y": 0.3741884249440639, "x": 5, "t": 1522016555.543216}, {"y": 0.06684808042190538, "x": 6, "t": 1522016557.546104}, {"y": 0.17399442194131343, "x": 7, "t": 1522016559.54899}, {"y": 0.025055174467733865, "x": 8, "t": 1522016561.551384}]'
    fo.write("%s\r\n" %val)
    return "done"

@app.route('/read/<string:num>')
def readmyfile(num):
    fo = open("static/files/test.txt","r")
    rows = fo.readlines()
    return rows[int(num)-1]


def background_thread(args):
    count = 0  
    dataCounter = 0 
    dataList = [] 
    distances = []
    obstacles = []
    
    ser = serial.Serial("/dev/ttyACM0", 9600)
    ser.baudrate = 9600
                    
    while True:
        try:
            read_ser = ser.readline().strip().decode("utf-8").split(',')
            
            distance = read_ser[0]
            obstacle = read_ser[1]
            servo = read_ser[2]
            distances.append(distance)
            obstacles.append(obstacle)
            
            #print("Distance: ", distance)
            #print("Obstacle: ", obstacle)
            #print("")
            print("Dist: " + distance + "Obst: " + obstacle + "Servo: "+ servo)
            socketio.emit('my_response', {'count':count, 'distance':distance, 'obstacle':obstacle, 'servo':servo}, namespace='/test')
            count = count +1
        except Exception:
            pass # or continue
         
    db.close()

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
    


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html', async_mode=socketio.async_mode)
    

@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['A'] = message['value']    
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})

@socketio.on('db_event', namespace='/test')
def db_message(message):   
#    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['db_value'] = message['value']    
#    emit('my_response',
#         {'data': message['value'], 'count': session['receive_count']})

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
   # emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
