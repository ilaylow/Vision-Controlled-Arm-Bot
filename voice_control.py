import speech_recognition as sr
import Adeept
import time
from transcribe import get_auth, get_url, on_message, on_close, on_error, on_open, parse_args, pix_send1, pix_send2, pix_send3, pix_send4, pix_send5

import argparse
import base64
import configparser
import json
import threading
import time

import pyaudio
import websocket
from websocket._abnf import ABNF

def serial_connect():    #Call this function to connect with the server
    global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr,ser
    com="COM3"    #Get the IP address from Entry
    Adeept.com_init(com,115200,1)
    Adeept.wiat_connect()
    Adeept.three_function("'servo_attach'",0,9)
    Adeept.three_function("'servo_attach'",1,6)
    Adeept.three_function("'servo_attach'",2,5)
    Adeept.three_function("'servo_attach'",3,3)
    Adeept.three_function("'servo_attach'",4,11)
    print(com+':Success')

# Importing from Transcribe.py from IBM Watson's Repository
CHUNK = 1024
FORMAT = pyaudio.paInt16
# Even if your default input is multi channel (like a webcam mic),
# it's really important to only record 1 channel, as the STT service
# does not do anything useful with stereo. You get a lot of "hmmm"
# back.
CHANNELS = 1
# Rate is important, nothing works without it. This is a pretty
# standard default. If you have an audio device that requires
# something different, change this.
RATE = 44100
RECORD_SECONDS = 5
FINALS = []
LAST = None

REGION_MAP = {
    'us-east': 'gateway-wdc.watsonplatform.net',
    'us-south': 'stream.watsonplatform.net',
    'eu-gb': 'stream.watsonplatform.net',
    'eu-de': 'stream-fra.watsonplatform.net',
    'au-syd': 'gateway-syd.watsonplatform.net',
    'jp-tok': 'gateway-syd.watsonplatform.net',
}

def main():
    serial_connect()

    pix_send1(None, 90)
    pix_send2(None, 90)
    pix_send3(None, 90)
    pix_send4(None, 90)
    pix_send5(None, 65)

    # Connect to websocket interfaces
    headers = {}
    userpass = ":".join(get_auth())
    headers["Authorization"] = "Basic " + base64.b64encode(
        userpass.encode()).decode()
    url = get_url()

    # If you really want to see everything going across the wire,
    # uncomment this. However realize the trace is going to also do
    # things like dump the binary sound packets in text in the
    # console.
    #
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                header=headers,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.args = parse_args()
    # This gives control over the WebSocketApp. This is a blocking
    # call, so it won't return until the ws.close() gets called (after
    # 6 seconds in the dedicated thread).
    ws.run_forever()

if __name__ == "__main__":
    main()