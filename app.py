import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
startDistance = None
scale = 0
cx, cy = 500, 500

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    # Overlay an image on the camera feed
    img1 = cv2.imread("kerala2.png")

    # Detect the zoom gesture
    if len(hands) == 2:
        # print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:
            print("zoom gesture")
            lmlist1 = hands[0]["lmList"]
            lmlist2 = hands[1]["lmList"]

            # Point 8 is the tip of index finger
            if startDistance is None:
                length, info, img = detector.findDistance(lmlist1[8][0:2], lmlist2[8][0:2], img)
                print(f"{length=}")
                startDistance = length

            length, info, img = detector.findDistance(lmlist1[8][0:2], lmlist2[8][0:2], img)
            scale = int(length - startDistance) // 2
            cx, cy = info[4:]
            print(f"{scale=}")
        else:
            startDistance = None

    try:
        h1, w1, _ = img1.shape
        newH, newW = ((h1+scale)//2)*2, ((w1+scale)//2)*2
        img1 = cv2.resize(img1, (newW, newH))

        img[cy-newH//2:cy + newH//2, cx-newW//2:cx + newW //2] = img1
        #img[10:177, 10:333] = img1
    except:
        pass


    cv2.imshow("image", img)
    cv2.waitKey(1)
