import cv2
import cvzone
import time
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
from playsound import playsound
from threading import Thread
import threading

#Library Code
#Firstly py get-pip.py (Install Pip)
#pip install opencv-python
#pip install cvzone
#pip install playsound
#pip install cmake
#pip install dlib
#pip install mediapipe






# For run same thread more than one.
class MTThread(Thread):
    def __init__(self, name="", target=None, args=()):

        self.args = args
        self.mt_name = name
        self.mt_target = target
        Thread.__init__(self, name=name, target=target, args=args)

    def start(self):
        super().start()
        Thread.__init__(self, name=self.mt_name,
                        target=self.mt_target, args=self.args)

    def run(self):
        super().run()
        Thread.__init__(self, name=self.mt_name,
                        target=self.mt_target, args=self.args)

    def join(self):
        super().join()
        Thread.__init__(self, name=self.mt_name,
                        target=self.mt_target, args=self.args)

# For check variables and run alarm.


def runAlarm(averageOfEye, isAlarmThreadWorked, isEyeOpen, ratioAvg_for_head, ratioAvg_for_mouth):
    print(f"AverageOfEye: {averageOfEye}  | isAlarmThreadWorked : {isAlarmThreadWorked} | eyecheck : {isEyeOpen} | headcheck: {ratioAvg_for_head} | mountCheck : {ratioAvg_for_mouth}")
    print(f"Active Thread: {threading.active_count()}")
    if ratioAvg_for_head <= 116 and threading.active_count() < 2:
        alarmThread.start()
    elif ratioAvg_for_mouth >= 60 and threading.active_count() < 2:
        alarmThread.start()

    elif averageOfEye <= 33 and isAlarmThreadWorked == True and isEyeOpen == False and threading.active_count() < 2:
        alarmThread.start()


def checkSleep():
    time.sleep(3)


sleepThread = MTThread(name="Sleep Thread", target=checkSleep)
alarmThread = MTThread(name="Alarm Thread",
                       target=playsound, args=("alarm.wav",))


def detect():
    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector(maxFaces=2)
    plotY_for_mouth = LivePlot(640, 360, [20, 60], invert=True)
    plotY_for_head = LivePlot(320, 360, [100, 200], invert=True)
    checkEyeLoop = True
    checkAlarmThread = True
    isAlarmThreadWorked = True
    isEyeOpen = True
    checkHeadLoop = True
    checkMouthLoop = True
    idList = [
        # Head Id List
        227, 34, 139, 21, 54, 103, 67, 109, 10, 338, 297, 332, 284, 301, 368,
        356, 447, 137, 177, 215, 138, 135, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 367, 435, 401, 366,

        # Eye Id List
        22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243, 286, 258, 257, 254, 259, 255, 467, 252, 253, 254, 341,

        # Mount Id List
        146, 91, 181, 84, 17, 314, 405, 321, 375, 409, 269, 267, 0, 37, 39, 185, 62, 325
    ]

    ratioList_for_mouth = []
    ratioList_for_head = []
    ratioList_for_eye = []
    while True:

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:

            face = faces[0]
            for id in idList:
                cv2.circle(img, face[id], 2, (255, 0, 255), cv2.FILLED)

            edgeLeft = face[62]
            edgeRight = face[325]

            MouthUp = face[0]
            MouthDown = face[17]

            lenghtVerMouth, _ = detector.findDistance(MouthUp, MouthDown)
            lenghtHoredge, _ = detector.findDistance(edgeLeft, edgeRight)
            # ----------------- MOUTH -----------------
            ratio = int((lenghtVerMouth / lenghtHoredge) * 100)
            ratioList_for_mouth.append(ratio)

            if len(ratioList_for_mouth) > 15:
                ratioList_for_mouth.pop(0)
            ratioAvg_for_mouth = sum(
                ratioList_for_mouth) / len(ratioList_for_mouth)

            cv2.line(img, MouthUp, MouthDown, (0, 200, 0), 2)
            cv2.line(img, edgeLeft, edgeRight, (0, 200, 0), 2)

            # ------------------ HEAD ---------------------
            Headup = face[10]
            Headdown = face[152]

            sideleft = face[227]
            sideright = face[447]

            lenghtVerside, _ = detector.findDistance(sideleft, sideright)
            lenghtHorHead, _ = detector.findDistance(Headup, Headdown)

            cv2.line(img, Headup, Headdown, (0, 200, 0), 2)
            cv2.line(img, sideright, sideleft, (0, 200, 0), 2)

            ratio = int((lenghtHorHead/lenghtVerside) * 100)
            ratioList_for_head.append(ratio)

            if len(ratioList_for_head) > 5:
                ratioList_for_head.pop(0)
            ratioAvg_for_head = sum(ratioList_for_head) / \
                len(ratioList_for_head)

            # ------------------ EYE ---------------------

            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]

            RightUp = face[257]
            RightDown = face[253]
            RightLeft = face[341]
            RightRight = face[467]

            lenghtVerLeft, _ = detector.findDistance(leftUp, leftDown)
            lenghtHorLeft, _ = detector.findDistance(leftLeft, leftRight)

            lenghtVerRight, _ = detector.findDistance(RightUp, RightDown)
            lenghtHorRight, _ = detector.findDistance(RightLeft, RightRight)

            cv2.line(img, leftUp, leftDown, (0, 200, 0), 2)
            cv2.line(img, leftLeft, leftRight, (0, 200, 0), 2)

            cv2.line(img, RightUp, RightDown, (0, 200, 0), 2)
            cv2.line(img, RightLeft, RightRight, (0, 200, 0), 2)

            ratio = int((lenghtVerLeft / lenghtHorRight) * 100)
            ratioList_for_eye.append(ratio)

            if len(ratioList_for_eye) > 5:
                ratioList_for_eye.pop(0)
            ratioAvg_for_eye = sum(ratioList_for_eye) / len(ratioList_for_eye)

            """*************************************************************************************"""

            cv2.putText(img, f"HAR :{str(int(ratioAvg_for_head))}", (
                10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(img, f"EAR :{str(int(ratioAvg_for_eye))}", (
                10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(img, f"MAR :{str(int(ratioAvg_for_mouth))}", (
                10, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            """ ------------------------ HEAD DETECT ------------------------ """
            if ratioAvg_for_head <= 116:
                cv2.putText(img, "Head Drowsiness Detected", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 3)
                if checkHeadLoop == True:
                    if checkAlarmThread == True:
                        sleepThread.start()
                        checkAlarmThread = False
                    checkHeadLoop = False
                else:
                    pass
            elif ratioAvg_for_head > 116 and checkHeadLoop == False:
                checkHeadLoop = True
                if not sleepThread.is_alive():
                    checkAlarmThread = True

            """ ------------------------ MOUTH DETECT ------------------------ """
            if ratioAvg_for_mouth >= 60:
                cv2.putText(img, "Mouth Drowsiness Detected", (10, 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 3)
                if checkMouthLoop == True:
                    if checkAlarmThread == True:
                        sleepThread.start()
                        checkAlarmThread = False
                    checkMouthLoop = False
                else:
                    pass
            elif ratioAvg_for_mouth <= 60 and checkMouthLoop == False:
                checkMouthLoop = True
                if not sleepThread.is_alive():
                    checkAlarmThread = True

            """ ------------------------ EYE DETECT ------------------------ """

            if ratioAvg_for_eye <= 33:
                cv2.putText(img, "Eye Drowsiness Detected", (10, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)
                isEyeOpen = False
                if checkEyeLoop == True:
                    if checkAlarmThread == True:
                        sleepThread.start()
                        checkAlarmThread = False
                        isAlarmThreadWorked = True
                    checkEyeLoop = False
                else:
                    pass
            elif ratioAvg_for_eye >= 33 and checkEyeLoop == False:
                checkEyeLoop = True
                isEyeOpen = True
                if not sleepThread.is_alive():
                    checkAlarmThread = True
                    isAlarmThreadWorked = False
            runAlarm(ratioAvg_for_eye, isAlarmThreadWorked,
                     isEyeOpen, ratioAvg_for_head, ratioAvg_for_mouth)
            #imgPlot_for_mouth = plotY_for_mouth.update(ratioAvg_for_eye)
            img = cv2.resize(img, (960, 480))
           # imgStack = cvzone.stackImages([img, imgPlot_for_mouth], 2, 1)
        else:
            img = cv2.resize(img, (960, 480))
            cv2.putText(img, "NO FACE DETECTED", (10, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
           # imgStack = cvzone.stackImages([img], 1, 1)

        cv2.imshow("Image", img)  # imgStack
        cv2.waitKey(25)


if __name__ == "__main__":
    detect()