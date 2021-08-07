import smtplib
from email.message import EmailMessage
import face_recognition
import cv2
import pickle
import pychromecast
import http.server
import multiprocessing

train_encodings = []
Names = []
scale_factor = 0.25

cast = pychromecast.Chromecast("192.168.1.42")
cast.wait()
print(cast.name)
mc = cast.media_controller
speak = True
mail = True
nameOld = ''

def caster(url):
    global speak 
    if speak == True: 
        mc.play_media(url, 'audio/mp3')
        mc.block_until_active()
        mc.pause()
        mc.play()
        speak = False

def email_alert(subject, body, to):
    global mail
    if mail == True:
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        
        user = "amanshastrychess@gmail.com"
        msg['from'] = user
        password = "okuzufnafknodfai"

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user,password)
        with open(r'login.jpg', 'rb') as f:
            image_data = f.read()
            image_name = f.name
            image_type = image_name.split(".")[1]
        msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        server.send_message(msg)
        server.quit()
        mail = False

def web_server():
    httpd = http.server.HTTPServer(server_address=('',8000),RequestHandlerClass=http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever(poll_interval=0.5)

with open ('train.pkl','rb') as f:
    Names = pickle.load(f)
    train_encodings = pickle.load(f)

print(Names)

cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while __name__ == '__main__':
    p = multiprocessing.Process(target=web_server, args=(), daemon=True)
    p.start()

    r,img = cam.read()
    img_small = cv2.resize(img,(0,0),fx = scale_factor,fy = scale_factor)
    img_rgb = cv2.cvtColor(img_small,cv2.COLOR_BGR2RGB)
    face_positions = face_recognition.face_locations(img_rgb,model = 'cnn')

    if not face_positions:
        continue

    all_encodings = face_recognition.face_encodings(img_rgb,face_positions)

    for (top,right,bottom,left),face_encoding in zip(face_positions,all_encodings):
        name = "Unknown person"
        matches = face_recognition.compare_faces(train_encodings,face_encoding)
        if True in matches:
            image_index = matches.index(True)
            name = Names[image_index]
            email = "Log in by: "+name
            url = "http://192.168.1.129:8000/"+name+".mp3"
            print(url)
            if name != nameOld:
                speak = True
                mail = True
            nameOld = name
            caster(url)
            top = int(top//scale_factor)
            left = int(left//scale_factor)
            bottom = int(bottom//scale_factor)
            right = int(right//scale_factor)
            cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),2)
            cv2.putText(img,name,(left,top),font,0.75,(0,255,0),thickness=2)
    
    cv2.imwrite("login.jpg",img)
    email_alert("Update",email,"amanshastrychess@gmail.com")