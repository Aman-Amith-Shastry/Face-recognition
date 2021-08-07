import pickle
import face_recognition
import os
import gtts

training_encodings = []
Names = []
image_dir =  r"C:\Users\91974\OneDrive\Desktop\all_other_stuff\Python\Open cv\known"

for root, dirs, files in os.walk(image_dir):
    for file in files:
        path = os.path.join(root,file)
        name = os.path.splitext(file)[0]
        person = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(person)[0]
        training_encodings.append(encoding)
        if "_" in name:
            name = name.split("_")[0]
        Names.append(name)
        print(name)
with open('train.pkl','wb') as f:
    pickle.dump(Names,f)
    pickle.dump(training_encodings,f)
print(Names)
    
for name in Names:
    msg = name+"is at the door"
    tts = gtts.gTTS(msg,lang="en",tld = "co.uk")
    url = name+".mp3"
    tts.save(url)

