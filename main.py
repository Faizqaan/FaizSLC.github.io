
import logging
import sys
from tkinter import Tk, messagebox
import eel
import base64
import cv2
import numpy as np
from camera import VideoCamera

# Set name of Video file to open. Leave name "" to open camera
video_name = "./web/image/Intruder-camera.mp4"
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# video_name = ""

startBool= False

# Read Images
img = cv2.imread("./web/image/empty.png",cv2.IMREAD_ANYCOLOR)

# Setup the images to display in html file
@eel.expose
def setup():
  img_send_to_js(img, "left")
 
#  Your code depend on image processing
# This is a sample code to change 
# and send processed image to JavaScript  
@eel.expose
def video_feed():
  process(x)

 
# Get Camera from video feed
# Add ur codes to process here
def process(camera):
  global startBool, outmp4

  strFilename = "Faiz-intruderDetect.mp4"
  #Create VideoWrite based on input image size
  success, frame = camera.get_frame()
  if success == True:
    outmp4 = cv2.VideoWriter(strFilename, cv2.VideoWriter_fourcc(*'mp4v'), 24, (frame.shape[1], frame.shape[0]))

  
  while True:
    success, frame = camera.get_frame()
      
    if success == True:
      startBool = True
      
      # Display Original Frame 
      text_send_to_js("Video Started", "p1")
      #img_send_to_js(frame, "left")

    
      #Perform your processing here
      imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
      faces = faceCascade.detectMultiScale(imgGray, scaleFactor = 1.1, minNeighbors=10, minSize=(5,5))

      for (x, y, w, h) in faces:
       faceRoiGray = imgGray[y: y + h, x: x + w]
       cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 0, 255),thickness=2)  
      
      imDisplay = frame.copy() 

      #Check if imDisplay is Grayscale. Convert to RGB if GrayScale                                                                                                                                                                      
      if(len(imDisplay.shape)<3):
       imDisplay = cv2.cvtColor(imDisplay, cv2.COLOR_GRAY2BGR) 

      sText = "Faiz Face Detect" 
      cv2.putText(imDisplay, sText, (20, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=1)
      img_send_to_js(imDisplay,"left")
    
      #Write to File
      outmp4.write(imDisplay)
      

    else:
      if startBool == False:
       text_send_to_js("Error in Starting Video ", "p1")
      break

    

# Stop Video Caturing
# Do not touch
@eel.expose
def stop_video_feed():
  x.stop_capturing()
  text_send_to_js("Video Stopped", "p1")
  
# Restart Video Caturing
# Do not touch
@eel.expose
def restart_video_feed():
  x.restart_capturing()
  process(x)
  text_send_to_js("Video Started", "p1")

@eel.expose
def save_video_feed():
  global outmp4
  outmp4.release()
  text_send_to_js("Video Saved you may exit now", "p1")

# Send text from python to Javascript 
# Do not touch
def text_send_to_js(val,id):
  eel.updateTextSrc(val,id)()

# Send image from python to Javascript 
# Do not touch
def img_send_to_js(img, id):
  if np.shape(img) == () :
    
    eel.updateImageSrc("", id)()
  else:
    ret, jpeg = cv2.imencode(".jpg",img)
    jpeg.tobytes()
    blob = base64.b64encode(jpeg) 
    blob = blob.decode("utf-8")
    eel.updateImageSrc(blob, id)()

# Start function for app
# Do not touch
def start_app():
  try:
    start_html_page = 'index.html'
    eel.init('web')
    logging.info("App Started")

    eel.start('index.html', size=(1000, 800))

  except Exception as e:
    err_msg = 'Could not launch a local server'
    logging.error('{}\n{}'.format(err_msg, e.args))
    show_error(title='Failed to initialise server', msg=err_msg)
    logging.info('Closing App')
    sys.exit()

if __name__ == "__main__":
  x = VideoCamera(video_name)
  start_app()