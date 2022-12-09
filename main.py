import face_recognition
import picamera
import numpy as np
from itertools import compress
from emailSender import sendEmailAlert
import time 
from threading import Thread
from webServer import startServer
import pickle
import movement


Thread(target=startServer).start()

Thread(target=movement.movement_detection).start()

print("Loading known faces")
with open("known_faces.npy", "rb") as f:
    known_faces = pickle.load(f)
    #known_faces = np.load(f, allow_pickle=True)

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
print("Camera initialization")
camera = picamera.PiCamera()
h=576
w=736
camera.resolution = (w, h)
output = np.empty((h, w, 3), dtype=np.uint8)

# Initialize some variables
face_locations = []
face_encodings = []
now = time.time() - 100
i=1
while True:
    if i>=50:
        i=0
    if i%5==0:
        print("Reloading known faces")
        with open("known_faces.npy", "rb") as f:
            known_faces = pickle.load(f)
            #known_faces = np.load(f, allow_pickle=True)
    i+=1
    print("Capturing image")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    
    # Find all the faces and face encodings in the current frame of video
    print("Finding faces...")
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        try:
            match = face_recognition.compare_faces((known_faces[0]), face_encoding)
        except:
            match = face_recognition.compare_faces(list(known_faces[0]), face_encoding)
        match_indexes = list(compress(range(len(match)), match))
        name = None
        if len(match_indexes)>0:
            name = known_faces[1][match_indexes[0]] 

        print("There's someone named {}!".format(str(name)))
        
        if int(time.time() - now)>20: # email each 20s with pic
            try:
                print(sendEmailAlert("Your camera detected someone.", output, name))
            except:
				print("Can't send email. ")
            now=time.time()
