import os
import cv2
import mediapipe as mp

# initialize Pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.95,
    min_tracking_confidence=0.95)

def loop_files(directory):
<<<<<<< HEAD
    f = open("correctSquat.py", "w")
=======
    f = open("wrongskeleton.py", "w")
>>>>>>> a92f2c0d6cd15847c12c5918111f29d365345a8a
    f.write("from dollarpy import Recognizer, Template, Point\n")
    recstring=""
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            if file_name.endswith(".mp4"):
                print(file_name)
                foo = file_name[:-4]
                recstring+=foo+","
                f.write (""+foo+" = Template('"+foo+"', [\n")
                # create capture object
                cap = cv2.VideoCapture(directory+"/"+file_name)
                framecnt=0
                while cap.isOpened():
                    # read frame from capture object
                    ret, frame = cap.read()
                    if not ret:
                        print("Can't receive frame (stream end?). Exiting ...")
                        break
                    frame = cv2.resize(frame, (640, 360))
                    framecnt+=1
                    
                    # convert the frame to RGB format
                    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    print (framecnt)
                    # process the RGB frame to get the result
                    results = pose.process(RGB)
                    image_height, image_width, _ = frame.shape
                    for i in (11, 32):
                        x = str(int(results.pose_landmarks.landmark[i].x*image_width))
                        y = str(int(results.pose_landmarks.landmark[i].y*image_height))
                        f.write ("Point("+x+","+y+", 1),\n")  
                    #print(f'Nose coordinates: ('
                    #    f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width}, '
                    #    f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_hight})'
                    #    )
                    #print(results.pose_landmarks)
                    # draw detected skeleton on the frame
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    # show the final output
                    cv2.imshow('Output', frame)
                    
                    if cv2.waitKey(1) == ord('q'):
                            break
                f.write ("])\n")    
                cap.release()
                cv2.destroyAllWindows()
    recstring = recstring[:-1]
    f.write ("recognizer = Recognizer(["+recstring+"])\n")    
    f.close()
