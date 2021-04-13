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

## Globals
srvIP       = "127.0.0.1"
srvPort     = "8080"
srvTout  = 10

jsonHeaders = {'Content-type' : 'application/json'}
sensorUID   = '1000'  # TODO: get UID from MAC address + PID


def connectServer(serverIP, serverPort):
    jsonData = json.dumps({ 'sensor_uuid' : sensorUID })
    httpConn = http.client.HTTPConnection(serverIP, serverPort, timeout=srvTout)
    httpConn.request('POST', '/connect_sensor', jsonData, jsonHeaders)
    connResponce = httpConn.getresponse()
    
    print("[INFO] Connection to HTTP server ", connResponce.read().decode())

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
        
def simple_mokup():
        conn = http.client.HTTPConnection('127.0.0.1', 8080, timeout=10)
        #this heather defines type of hatt data= json 
        headers = {'Content-type' : 'application/json'} 
        #an example for json
        json_txt = {"buffer": [
                    {'id' : '001', 'date' : '30.04.1968 12:55', 'status' : '0'},
                    {'id' : '001', 'date' : '30.04.1968 12:56', 'status' : '1'},
                    {'id' : '001', 'date' : '30.04.1968 12:57', 'status' : '1'},
                    {'id' : '001', 'date' : '30.04.1968 12:58', 'status' : '0'},
                    {'id' : '001', 'date' : '30.07.1968 12:58', 'status' : '2'},
                    {'id' : '001', 'date' : '30.06.1968 12:58', 'status' : '2'},
                    {'id' : '001', 'date' : '30.05.1968 12:58', 'status' : '2'},
                    {'id' : '001', 'date' : '31.04.1968 12:58', 'status' : '0'},
                    {'id' : '001', 'date' : '30.04.1968 12:59', 'status' : '2'}
                    ]
        }
        #dumps- converts text to jason 
        json_data = json.dumps(json_txt)
        
        #sends request to the server 
        conn.request('POST', '/send_buffer', json_data, headers)
        
        response = conn.getresponse()
        print(response.read().decode())

def sensor_check_masking(frame, faceNet, maskNet):
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

## MAIN @@
srv_ip = "127.0.0.1"
srv_port = "8080"
srv_conn_imeout = 10

# Init HTTP connection to the server
connectServer(srvIP, srvPort)

# TODO: process possible errors here

# Init CV supplimentary components

# Load serialized face detector model from disk
faceDetectorDir = r"face_detector"
prototxtPath = os.path.join(faceDetectorDir, "deploy.prototxt")
weightsPath  = os.path.join(faceDetectorDir, "res10_300x300_ssd_iter_140000.caffemodel")

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model("mask_detector.model")

# initialize the video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()


while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
##(locs, preds) = detect_and_:split predict_mask(frame, faceNet, maskNet)
        (locs, preds) = sensor_check_masking(frame, faceNet, maskNet)


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
        if key == ord("q"):
                break

        ##time.sleep(2)

print("[DEBUG] exit from process 1")
# do a bit of cleanup
cv2.destroyAllWindows()
print("[DEBUG] exit from process 2")
vs.stop()
print("[DEBUG] exit from process 3")
conn.close()
