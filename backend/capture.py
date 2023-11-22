import cv2

# turn into function that takes image and recording boolean as input

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # add here:
    # if recording
    # save frame to gcs
    # otherwise just display
        
    cv2.imshow('iSpy', frame)
    
    # edit this so break when not on page upload
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()