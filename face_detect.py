import cv2
import sys

# implementing a face cascade
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 

# sets video source to default webcam
video_capture = cv2.VideoCapture(0)

# captures the video one frame at a time
while True:
    ret, frame = video_capture.read()

    # converts color of the frame to bgr2gray model
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Note: detectMultiScale function is used to detect 
    # the faces. This function will return a list of 
    # rectangles (x,y,w,h) around the detected objects.
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5, 
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle on indentified faces given the coordinates onto frame
    # Usage: rectangle(start_point, end_point, color, thickness)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Display result
    cv2.imshow('Video', frame)

    # if the q key is pressed, we quit and exit the while loop
    # Usage: ord(character) extracts the unicode value of a character
    #        cv2.waitkey(delay) waits for a key to be pressed for delay seconds
    #                           and if a key is pressed, it returns a 32-bit integer
    #                           corresponding to the key
    #        & 0xFF is a bit mask which sets the left 24 bits to zero so that 
    #        the above two function return values can make a valid comparison
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleaning up once program is finished
video_capture.release()
cv2.destroyAllWindows()