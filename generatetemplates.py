import cv2
import mediapipe as mp
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose 
mphands = mp.solutions.hands

pose = mp_pose.Pose(
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)
hands = mphands.Hands()
def StartTest(directory):
    f = open("Templates.py", "a")
    f.write("from dollarpy import Recognizer, Template, Point \n")
    recstring = ""
    # loop over all files in directory, execute for videos only 
    for file_name in os.listdir(directory):
        if file_name.endswith(".mp4"):
            # f.write("\nresult = recognizer.recognize")
            #create capture object 
            print(file_name)
            foo = file_name[:-4]
            recstring+= foo+','
            f.write(""+foo+" = Template('"+foo+"', [\n")        
            cap = cv2.VideoCapture(directory +'/' + file_name)
            framecnt = 0
            while cap.isOpened() :
                #read frame from capture object 
                ret, frame = cap.read()
                if not ret :
                    print("Error cannot read frame exiting")
                    break
                frame = cv2.resize(frame, (480, 320))
                print(framecnt)
                
                frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (720, 400))
                results = hands.process(frame)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        image_height, image_width, _ = frame.shape
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks, mphands.HAND_CONNECTIONS
                        )
                        # need to modify loop to only get certain coordinates such as thumb and pointer finger only 
                        for ids, landmrk in enumerate(hand_landmarks.landmark):
                            x = str(int(landmrk.x*image_width))
                            y = str (int(landmrk.y * image_height))
                            f.write("Point("+x+", "+y+", 1), \n")
                            # x = str(int(results.multi_hand_landmarks.landmark.INDEX_FINGER_TIP.x*image_width))
                            # y = str (int(results.multi_hand_landmarks.landmark.INDEX_FINGER_TIP.y * image_height))
                            # f.write("Point("+x+", "+y+", 1), \n")
                            # x = str(int(results.multi_hand_landmarks.landmark.INDEX_FINGER_MCP.x*image_width))
                            # y = str (int(results.multi_hand_landmarks.landmark.INDEX_FINGER_MCP.y * image_height))
                            # f.write("Point("+x+", "+y+", 1), \n")
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imshow("handtracker", frame)

                if cv2.waitKey(1) == ord('q'):
                    break
            f.write("])\n")
            cap.release()
            cv2.destroyAllWindows()
    recstring = recstring [:-1]
    f.write("recognizer =  Recognizer(["+recstring+"])\n")
    f.close()

directory_path = "C:/Users/aliya/Desktop/tiral/"
StartTest(directory_path)
                        
                
                
                        
                
                    
                
                    
                
                
                
            
            
    
    