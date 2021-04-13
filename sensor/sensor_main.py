from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import cv2
import os
import http.client
from datetime import datetime
import time ## TODO: check and remove
import json
import glob
import argparse


## Globals
srvTout  = 10

jsonHeaders = {'Content-type' : 'application/json'}
sensorUID   = '1000'  # TODO: get UID from MAC address + PID

##---------------------------------------------------------------------

##
class FrameMaker:
    """
    Switching between data sources, depending on params
    
    Attributes
    ----------
    mode : int 
        data source selector. 
        0 - get data from video cam 
        1 - get the data from testing directory
    src : int
        number of video port
    src : string
        path to testing directory
        
    Methods
    -------
    read()
        reading one frame from data source and reduse it to appropriate size
    close()
        jently stop the imput device before finish
    """
    def __init__(self, mode, src):
        self.mode = mode
        if self.mode == 0: ## get frame from video input
            print("[DEBUG] initialie video sreeam as data source")
            self.default_vs = 0
            self.vs = VideoStream(src=0).start()
        elif self.mode == 1: ## get frame from pictures array source
            print("[DEBUG] initialise pictures array as data source")
            img_dir = os.path.join(src, '*.jpeg')
            self.ps = glob.glob(img_dir)
            self.index = 0
            self.max_index = len(self.ps)
        else:
            print("ERROR: wrong mode")
    
    def read(self):
    
        print("[DEBUG] FrameMaker config - mode = ", self.mode)
    
        if self.mode == 0:
            frame = self.vs.read()
        else:
            ## cyclic running on picture source
            if self.index == self.max_index :
                self.index = 0
                
            frame = cv2.imread(self.ps[self.index])
            self.index += 1
            
        frame = imutils.resize(frame, width=400)
        return frame

    def close(self):
        if self.mode == 0:
            frame = self.vs.stop()
            
        return None

def connectServer(serverIP, serverPort):
    jsonData = json.dumps({ 'sensor_uuid' : sensorUID })
    httpConn = http.client.HTTPConnection(serverIP, serverPort, timeout=srvTout)
    httpConn.request('POST', '/connect_sensor', jsonData, jsonHeaders)
    connResponce = httpConn.getresponse()
    
    print("[INFO] Connection to HTTP server %s:%s" % (serverIP, serverPort))  
    print(connResponce.read().decode())

def addBuffer(maskPeoples, nomaskPeoples):
    totalPeoples = maskPeoples + nomaskPeoples
    if totalPeoples != 0 :
        
        dataRec = {}
        dataRec['id'] = sensorUID
        dataRec['date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        dataRec['status'] = round((maskPeoples * 100) / totalPeoples)
        
        dataRecCopy = dataRec.copy()
        dataList.append(dataRecCopy)
        jsonText["buffer"] = dataList
        
        print("[DEBUG] output JSON is ", jsonText)
        jsonData = json.dumps(jsonText)
        httpConn = http.client.HTTPConnection(srvIP, srvPort, timeout=srvTout)
        httpConn.request('POST', '/send_buffer', jsonData, jsonHeaders)
        connResponce = httpConn.getresponse()
        print(connResponce.read().decode())
    else:
        print("DEBUG] no person found")
        
def checkMasking(frame, faceNet, maskNet):
        # grab the dimensions of the frame and then construct a blob
        # from it
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        faceNet.setInput(blob)
        detections = faceNet.forward()
        print(detections.shape)

        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        locs = []
        preds = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the detection
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the confidence is
                # greater than the minimum confidence
                if confidence > 0.5:
                        # compute the (x, y)-coordinates of the bounding box for
                        # the object
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        # ensure the bounding boxes fall within the dimensions of
                        # the frame
                        (startX, startY) = (max(0, startX), max(0, startY))
                        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                        # extract the face ROI, convert it from BGR to RGB channel
                        # ordering, resize it to 224x224, and preprocess it
                        face = frame[startY:endY, startX:endX]
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                        face = cv2.resize(face, (224, 224))
                        face = img_to_array(face)
                        face = preprocess_input(face)

                        # add the face and bounding boxes to their respective
                        # lists
                        faces.append(face)
                        locs.append((startX, startY, endX, endY))

        # only make a predictions if at least one face was detected
        if len(faces) > 0:
                # for faster inference we'll make batch predictions on *all*
                # faces at the same time rather than one-by-one predictions
                # in the above `for` loop
                faces = np.array(faces, dtype="float32")
                preds = maskNet.predict(faces, batch_size=32)

        # return a 2-tuple of the face locations and their corresponding
        # locations
        return (locs, preds)

# MAIN #
argParser = argparse.ArgumentParser()
argParser.add_argument('--i', type=str, help="IP address of the server", required=False, default='127.0.0.1')
argParser.add_argument('--p', type=str, help="Port to connect to the server", required=False, default='8080')
argParser.add_argument('--t', type=str, help="testing data directory", required=False)
argParser.add_argument('--D', help="Set up debug mode", action='store_true') # TODO: next-step feature
argsData = argParser.parse_args()

srvIP   = argsData.i
srvPort = argsData.p
dataDir = argsData.t

print("[DEBUG] data_dir: ", dataDir)

# Init HTTP connection to the server
connectServer(srvIP, srvPort)

# Load serialized face detector model from disk
faceDetectorDir = r"face_detector"
prototxtPath = os.path.join(faceDetectorDir, "deploy.prototxt")
weightsPath  = os.path.join(faceDetectorDir, "res10_300x300_ssd_iter_140000.caffemodel")

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model("mask_detector.model")

# initialize the data source

if dataDir != None :
    print("[INFO] data source is directory")
    fm = FrameMaker(1, 'test_data')
else:
    print("[INFO] data source is video stream...")
    fm = FrameMaker(0, 0)
    


while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        
        ##frame = vs.read()
        ##frame = imutils.resize(frame, width=400)
        frame = fm.read()

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = checkMasking(frame, faceNet, maskNet)

        maskPeoples = nomaskPeoples = 0

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
                # unpack the bounding box and predictions
                (startX, startY, endX, endY) = box
                (mask, withoutMask) = pred

                # determine the class label and color we'll use to draw
                # the bounding box and text
                label = "Mask" if mask > withoutMask else "No Mask"
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                
                if label == "Mask" :
                    maskPeoples += 1
                else:
                    nomaskPeoples += 1
                # include the probability in the label
                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                # display the label and bounding box rectangle on the output
                # frame
                cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        jsonText = {}
        dataList = []

        addBuffer(maskPeoples, nomaskPeoples)
            
        # show the output frame%
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(5000) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord('q'):
                break

# do a bit of cleanup
cv2.destroyAllWindows()
fm.close()
#httpConn.close()
