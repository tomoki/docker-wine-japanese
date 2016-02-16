from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import subprocess
import os
import threading
import random
import string

WHERE_IS_SPEECH_VOICEROID=os.path.join(os.path.dirname(os.path.realpath(__file__)), "speech_voiceroid.exe")
PORT=48234
lock = threading.Lock()

def play_in_voiceroid(speaker, message):
    with lock:
        print(message)
        prop = subprocess.Popen(["wine", WHERE_IS_SPEECH_VOICEROID, speaker, message])
        prop.wait()
    return

def save_in_voiceroid(speaker, message):
    with lock:
        wav = "".join([random.choice(string.ascii_letters) for i in range(5)]) + ".wav"
        wavpath_win = "c:\\users\\wine\\" + wav
        wavpath_lnx = "/home/wine/.wine/drive_c/users/wine/" + wav
        print(message + " " + wavpath_win + " " + wavpath_lnx)
        # it requires windows-like path.
        prop = subprocess.Popen(["wine", WHERE_IS_SPEECH_VOICEROID, speaker, message, wavpath_win])
        prop.wait()
        return wavpath_lnx


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        uri = self.path
        ret = parse_qs(urlparse(uri).query, keep_blank_values = True)
        message = ""
        speaker = ""
        def send_back_error(message):
            body = bytes('{"success":false}', "utf-8")
            self.send_response(200)
            # TODO: change content-type
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-length', len(body))
            self.end_headers()
            self.wfile.write(body)
            return


        if(not "message" in ret.keys()):
            return send_back_error("no message specified")
        if(not "speaker" in ret.keys()):
            return send_back_error("no speaker specified")

        message = ret["message"][0]
        speaker = ret["speaker"][0]
        direct = "direct" in ret.keys()

        if direct:
            play_in_voiceroid(speaker, message)
            body = bytes('{"success":true}', "utf-8")
            self.send_response(200)
            # TODO: change content-type
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-length', len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            path = save_in_voiceroid(speaker, message)
            body = open(path, "rb").read()
            # body = bytes('{"success":true}', "utf-8")
            self.send_response(200)
            # TODO: change content-type
            self.send_header('Content-Type', 'audio/x-wav')
            self.send_header('Content-length', len(body))
            self.end_headers()
            self.wfile.write(body)


httpd = HTTPServer(("", PORT), MyHandler)
httpd.serve_forever()
