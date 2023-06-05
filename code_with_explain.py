import boto3                                       #(Imports the Boto3 library, which is the AWS SDK (Software Development Kit) for Python. It allows interaction with various AWS services.)
import cv2                                         #(Imports the OpenCV library, which is a computer vision library used for image and video processing.)
from cvzone.HandTrackingModule import HandDetector #(Imports the 'HandDetector' class from the 'HandTrackingModule' module of the cvzone library. This module provides hand tracking functionality.)
detector = HandDetector(maxHands=1)                #(Creates an instance of the HandDetector class with a parameter 'maxHands' set to 1. This detector will be used to detect and track hands in the video stream.)
cap = cv2.VideoCapture(0)                          #(Creates a 'VideoCapture' object with index 0, which represents the default camera connected to the computer. This object will be used to capture video frames.)
status, photo =cap.read()                          #(Reads a frame from the video capture and assigns it to the variables 'status' and 'photo'. The 'status' variable indicates whether the frame was successfully read.)
allOS = []                                         #(Initializes an empty list called allOS. This list will be used to store the IDs of launched instances.)
ec2 = boto3.resource("ec2")                        #(Creates an EC2 (Elastic Compute Cloud) resource object using the Boto3 library. This object allows interaction with EC2 instances.)
def myOSLaunch():                                  #(Defines a function named 'myOSLaunch' which will be responsible for launching a new EC2 instance when 2 fingers are shown.)
    instances = ec2.create_instances(              #(Uses the 'create_instances' method of the 'ec2' resource object to launch a new EC2 instance. It specifies the image ID, minimum and maximum count of instances, instance type, and security group IDs. The created instances are assigned to the 'instances' variable.)
            ImageId="ami-0a2acf24c0d86e927",       
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            SecurityGroupIds=[ "sg-001319ebd08a4cadb" ] 
        )
    myid = instances[0].id                         #(Retrieves the ID of the first instance from the instances list and assigns it to the variable 'myid'.)
    allOS.append(myid)                             #(Appends the 'myid' value to the 'allOS' list, storing the ID of the launched instance.)
    print( "Total OS : ", len(allOS))              #(Prints the total number of instances in the 'allOS' list.)
    print(myid)                                    #(Prints the ID of the launched instance.)


def OSTerminate():                                 #(Defines a function named 'OSTerminate' which will be responsible for terminating the most recently launched EC2 instance.)
    osdelete = allOS.pop()                         #(Removes and retrieves the last element from the 'allOS' list and assigns it to the 'osdelete' variable. This represents the ID of the instance to be terminated.)
    response = ec2.instances.filter(InstanceId=[osdelete]).terminate() #(Uses the 'filter' method of the EC2 resource object to filter instances based on the instance ID ('osdelete'). Then, the 'terminate' method is called to terminate the filtered instance.)
    print("total os:", len(allOS))                 #(Prints the total number of instances remaining in the allOS list after termination.)
    


while True:                                        #(Starts an infinite loop.)
    status, photo = cap.read()                     #(Reads a frame from the video capture and assigns it to the variables 'status' and 'photo'.)
    cv2.imshow("myphoto", photo)                   #(Displays the 'photo' frame in a window with the title "myphoto" using 'cv2.imshow'.)
    if cv2.waitKey(34) == 13:                      #(Waits for a key event and checks if the key pressed is Enter (key code 13). If Enter is pressed, the loop breaks and the program exits.)
        break                                      
    hand = detector.findHands(photo , draw=False)  #(Uses the 'findHands' method of the 'detector' object to detect and track hands in the 'photo' frame. The 'draw' parameter is set to 'False' to disable drawing landmarks on the detected hands.)
    if hand:                                       #(Checks if hands are detected in the 'photo' frame.)
        lmlist = hand[0]                           #(Retrieves the list of landmarks (finger points) from the first detected hand and assigns it to the 'lmlist' variable.)
        totalFinger = detector.fingersUp(lmlist)   #(Uses the 'fingersUp' method of the 'detector' object to determine the number of fingers raised based on the landmarks ('lmlist'). The result is assigned to the 'totalFinger' variable.)
        if totalFinger == [0, 1, 1, 0, 0]:         #(Checks if the totalFinger list matches the pattern '[0, 1, 1, 0, 0]', which corresponds to two fingers raised.)
            print("2 finger up, starting 1 instance..........") #(Prints a message indicating that two fingers are raised, and a new instance is being launched.)
            myOSLaunch()                           #(Calls the 'myOSLaunch' function to launch a new EC2 instance.)
        elif totalFinger == [0, 1, 0, 0, 0]:       #(Checks if the 'totalFinger' list matches the pattern '[0, 1, 0, 0, 0]', which corresponds to one finger raised.)
            print("1 finger up, terminating 1 instance..........") #(Prints a message indicating that one finger is raised, and the most recently launched instance is being terminated.)
            OSTerminate()                          #(Calls the 'OSTerminate' function to terminate the most recently launched EC2 instance.)
        else:                                      #(Executes if none of the previous conditions are met.)
            print("no signal given")               #(Prints a message indicating that no recognized hand signal is given.)
cv2.destroyAllWindows()                            #(Closes all OpenCV windows.)
cap.release()                                      #(Releases the video capture object and frees the associated resources.)
