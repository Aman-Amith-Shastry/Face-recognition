# Face-recognition
Using the open CV module in python, combined with the face recognition module to develop a real time face recognition program
Features:
1. Email to user
2. Alert the user by sending a message to Google Home
3. Can be easily used with a micro computer such as Jetson Nano or Raspberry Pi

Getting training data:
  1. Make a directory to store all the images of the registered people
  2. Upload and run the code to save the face encodings of each induvidual in the images as a pickle file
  *Note: Images in the training dataset should be of induvidual people only
 
 Use training data to compare faces:
  1. Upload and run code to load camera and compare the encodings of the face detected to the loaded training data
  2. If a face is detected, alert the user by sending a message to Google Home and an email
  3. If no face is detected, remain dormant
