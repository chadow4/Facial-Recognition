import face_recognition
import numpy as np

# Load a sample picture and learn how to recognize it.

obama_image = face_recognition.load_image_file("obama_small.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

known_faces=np.array([[obama_face_encoding, biden_face_encoding], ["Barack Obama", "Joe Biden"]])
with open("known_faces.npy", "wb") as f:
    np.save(f, known_faces, allow_pickle=True)