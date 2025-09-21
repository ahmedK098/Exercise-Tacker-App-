import cv2
import mediapipe as mp
from dollarpy import Recognizer, Template, Point
import csv
from datetime import date
import math

from correcttemplate import recognizer
from wrongtemplate import recognizer2

correcttemplate = ['squat1', 'squat2', 'squat3', 'squat4', 'squat5', 'squat6', 'squat7', 'squat8', 'squat9', 'squat10', 'squat11', 'squat12']
wrongtemplate = ['w_squat1', 'w_squat2', 'w_squat3', 'w_squat4', 'w_squat5', 'w_squat6']


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

# Wrong and correct reps count
reps = 0
w_reps = 0

startingPose = 0

squatting = False
finsihed_Squatt = False

today = date.today()
cap = cv2.VideoCapture(0)
framecnt = 0
# empty array to hold points of detected poses
points = []
while cap.isOpened():
    #read frame object 
    ret, frame = cap.read()
    if not ret :
        print("Cannot recieve frame Exiting")
        break
    framecnt+=1
    # resize frame 
    frame = cv2.resize(frame, (640, 360))
    #convert frame to RGB format
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # print(framecnt)
    results = pose.process(RGB)
    image_height, image_width, _ = frame.shape
    # left and right shoulder coordinates
    if results.pose_landmarks :
        #Set the starting position
        if startingPose == 0:
            startingPose = math.dist(
                (results.pose_landmarks.landmark[23].x, results.pose_landmarks.landmark[23].y),
                (results.pose_landmarks.landmark[29].x, results.pose_landmarks.landmark[29].y)
            )
            
        currentPose = math.dist(
                (results.pose_landmarks.landmark[23].x, results.pose_landmarks.landmark[23].y),
                (results.pose_landmarks.landmark[29].x, results.pose_landmarks.landmark[29].y)
        )
        
        # Check for start of squat
        if currentPose < startingPose * 0.9 and not squatting:
            squatting = True
            finsihed_Squatt = False

        # Collect points during the squat
        if squatting:
            for i in (11, 32):
                x = int(results.pose_landmarks.landmark[i].x * image_width)
                y = int(results.pose_landmarks.landmark[i].y * image_height)
                points.append(Point(x, y, 1))
        
        # Check for end of squat (user returns to standing)
        if currentPose > startingPose * 0.95 and squatting and not finsihed_Squatt:
            finsihed_Squatt = True
            squatting = False

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Check the form an give the result
        if finsihed_Squatt:
            result = recognizer.recognize(points)
            print(result)
            framecnt = 0
            if result[0] in correcttemplate and result[1] > 0.5:
                reps += 1 
            else:
                w_reps+=1
            points.clear()
            finsihed_Squatt = False
    cv2.putText(frame, "Reps: " + str(reps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, "Wrong Reps: " + str(w_reps), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # show output in real time
    cv2.imshow('Output', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
print(reps)
print(w_reps)
# header = ['Date/Videoname idk', 'Correct rep count']
row = [today, reps, w_reps]
with open('output.csv', 'a', newline = '') as file :
    writer = csv.writer(file)
    # writer.writerow(header)
    writer.writerow(row)