from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import subprocess
import os
import threading

WHERE_IS_SPEECH_VOICEROID=os.path.join(os.path.dirname(os.path.realpath(__file__)), "speech_voiceroid.exe")
PORT=48234
lock = threading.Lock()

def play_in_voiceroid(speaker, message):
    with lock:
        print(message)
        prop = subprocess.Popen(["wine", WHERE_IS_SPEECH_VOICEROID, speaker, message])
        prop.wait()
    return


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        uri = self.path
        ret = parse_qs(urlparse(uri).query, keep_blank_values = True)
        message = ""
        speaker = ""

        if("message" in ret.keys()):
            message = ret["message"][0]
        if("speaker" in ret.keys()):
            speaker = ret["speaker"][0]

        body = bytes("", "utf-8")
        if(speaker != "" and message != ""):
            play_in_voiceroid(speaker, message)
            body = bytes('{"success":true}', "utf-8")
        else:
            body = bytes('{"success":false}', "utf-8")

        self.send_response(200)
        # TODO: change content-type
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)

host = '0.0.0.0'
httpd = HTTPServer(("", PORT), MyHandler)
httpd.serve_forever()
