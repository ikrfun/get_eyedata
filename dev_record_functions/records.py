import pandas as pd
from pynput.keyboard import Key, Listener
from datetime import datetime

class KeyLogger:
    def __init__(self):
        self.df = pd.DataFrame(columns=['time', 'key'])
        self.listener = None

    def on_press(self, key):
        self.df = self.df.append({'time': datetime.now(), 'key': str(key)}, ignore_index=True)

    def start_record(self):
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def stop_record(self):
        if self.listener is not None:
            self.listener.stop()
        # Save the dataframe to a csv file
        self.df.to_csv('key_log.csv', index=False)

        # Clear the dataframe and the listener
        self.df = pd.DataFrame(columns=['time', 'key'])
        self.listener = None

import pandas as pd
from pynput.mouse import Listener
from datetime import datetime
import math

class MouseLogger:
    def __init__(self):
        self.df = pd.DataFrame(columns=['time', 'x', 'y', 'x_change', 'y_change'])
        self.listener = None
        self.last_position = (0, 0)

    def on_move(self, x, y):
        x_change = x - self.last_position[0]
        y_change = y - self.last_position[1]
        self.df = self.df.append({'time': datetime.now(), 'x': x, 'y': y, 
                                   'x_change': x_change, 'y_change': y_change}, 
                                  ignore_index=True)
        self.last_position = (x, y)

    def start_record(self):
        self.listener = Listener(on_move=self.on_move)
        self.listener.start()

    def stop_record(self):
        if self.listener is not None:
            self.listener.stop()
        # Save the dataframe to a csv file
        self.df.to_csv('mouse_log.csv', index=False)

        # Clear the dataframe and the listener
        self.df = pd.DataFrame(columns=['time', 'x', 'y', 'x_change', 'y_change'])
        self.listener = None

import websocket
import json

class ObsController:
    def __init__(self, address):
        self.ws = websocket.create_connection(address)
        
    def send_message(self, message):
        self.ws.send(json.dumps(message))
        
    def start_recording(self):
        message = {
            "request-type": "StartRecording",
            "message-id": "1"
        }
        self.send_message(message)
        
    def stop_recording(self):
        message = {
            "request-type": "StopRecording",
            "message-id": "2"
        }
        self.send_message(message)

    def close_connection(self):
        self.ws.close()

import zmq
import msgpack
import pandas as pd
from time import time

class PupilController:
    def __init__(self):
        self.context = zmq.Context()
        # open a req port to talk to pupil
        self.addr = '127.0.0.1'  # remote ip or localhost
        self.req_port = "50020"  # same as in Pupil Remote
        self.req = self.context.socket(zmq.REQ)
        self.req.connect(f"tcp://{self.addr}:{self.req_port}")

        # ask for the sub port
        self.req.send_string('SUB_PORT')
        self.sub_port = self.req.recv_string()

        # open a sub port to listen to pupil
        self.sub = self.context.socket(zmq.SUB)
        self.sub.connect(f"tcp://{self.addr}:{self.sub_port}")

        # subscribe to pupil data (topic: 'pupil')
        self.sub.setsockopt_string(zmq.SUBSCRIBE, 'pupil')

        self.df = pd.DataFrame(columns=['timestamp', 'norm_pos_x', 'norm_pos_y'])

    def start_recording(self):
        self.req.send_string('R')
        print(self.req.recv_string())

    def stop_recording(self):
        self.req.send_string('r')
        print(self.req.recv_string())

    def record_pupil_data(self, duration):
        start_time = time()
        while time() - start_time < duration:
            topic, msgpack_serialized_payload = self.sub.recv_multipart()
            payload = msgpack.loads(msgpack_serialized_payload, raw=False)
            self.df = self.df.append({
                'timestamp': payload['timestamp'],
                'norm_pos_x': payload['norm_pos'][0],
                'norm_pos_y': payload['norm_pos'][1]
            }, ignore_index=True)

        # Save the dataframe to a csv file
        self.df.to_csv('pupil_data.csv', index=False)

