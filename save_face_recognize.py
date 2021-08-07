import pickle
import face_recognition
import os
import pickle
import gtts

from face_recognition.api import face_locations

training_encodings = []
Names = []
image_dir =  r" *Your directory of known images* "

for root, dirs, files in os.walk(image_dir):
    for file in files:
        path = os.path.join(root,file)
        name = os.path.splitext(file)[0]
        person = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(person)[0]
        training_encodings.append(encoding)
        Names.append(name)
        print(name)
        print(encoding)

for name in Names:
    msg = name+"is at the door"
    tts = gtts.gTTS(msg,lang="en",tld = "co.uk")
    url = name+".mp3"
    tts.save(url)

with open('train.pkl','wb') as f:
    pickle.dump(Names,f)
    pickle.dump(training_encodings,f)
