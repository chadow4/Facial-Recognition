from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote
import base64
import os
import face_recognition
import numpy as np
import subprocess
import pickle

hostName = "127.0.0.1"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path[:5] == "/add?":
            query = urlparse(self.path).query
            q = dict((qc.split("=")) for qc in query.split("&"))
            if os.path.isfile("images/"+q["file"]):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.pushString("<html><head><title>Add someone</title></head><body>")
                if ("personName" in q.keys() and q["personName"]!=""):
                    # add 
                    biden_image = face_recognition.load_image_file("images/"+q["file"])
                    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
                    with open("known_faces.npy", "rb") as f:
                        known_faces = pickle.load(f)
                        #known_faces = np.load(f, allow_pickle=True)
                    fae=list(known_faces[0])
                    fae.append(biden_face_encoding)
                    fae=np.array(fae)
                    fan=list(known_faces[1])
                    fan.append(unquote(q["personName"]).replace("+", " "))
                    #fan=np.array(fan)
                    known_faces = [fae, fan]
                    with open("known_faces.npy", "wb") as f:
                        p = pickle.Pickler(f)
                        p.dump(known_faces)
                        #np.save(f, known_faces, allow_pickle=True)
                    self.pushString("<h3>Picture of "+str(q["personName"]).replace("+", " ")+" saved.</h3>")
                    self.pushString("<p>This tab should close itself in 10 seconds.</p>")
                    self.pushString("<script>setTimeout('window.close()',10000) </script>")
                    os.remove("images/"+q["file"]) #delete file as it's useless
                else:
                    with open("images/"+q["file"], "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    self.pushString("<h1>Who is : </h1>") #self.path
                    self.pushString('<div><img style="max-width:100%;" src="data:image/jpeg;base64, '+encoded_string.decode("utf-8")+'" alt="Unknown person"></div>')
                    self.pushString("<br><form><input type='hidden' name='file' value='"+q["file"]+"'><input required name='personName' type='text' placeholder='Person Name'><button>Send</button></form>")
                self.pushString("</body></html>")
        else:
            self.send_response(404)
            self.end_headers()
    def pushString(self, s : str):
        self.wfile.write(bytes(s, "utf-8"))

def startServer():        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Webserver stopped.")

