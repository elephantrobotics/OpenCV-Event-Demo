from camera import OrbbecCamera
from aruco_detector import ArucoDetector
import cv2
import time

cam = OrbbecCamera(0)
aruco_detector = ArucoDetector()

while True:
    if cam.update_frame():
        bgr_frame = cam.get_bgr_frame()
        ids, corners = aruco_detector.detect_marker_corners(bgr_frame)
        visu_frame = aruco_detector.visualize(bgr_frame, ids, corners)
        cv2.imshow("Test", visu_frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(0.01)
