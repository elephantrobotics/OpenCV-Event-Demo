from camera import OrbbecCamera
from utils import crop_frame
from aruco_detector import ArucoDetector
import cv2
import time
import numpy as np

cam = OrbbecCamera(0)
aruco_detector = ArucoDetector()

while True:
    if cam.update_frame():
        bgr_frame = cam.get_bgr_frame()
        ids, corners = aruco_detector.detect_marker_corners(bgr_frame)

        if len(ids) == 0 and len(corners) == 0:
            print("No aruco found.")
            continue

        corners = corners.astype(np.int32)
        marker_info = zip(ids, corners)
        marker_info = list(filter(lambda x: x[0] == 0, marker_info))
        if len(marker_info) != 2:
            print(f"Anchor point error, should have 2 anchor points, got {len(marker_info)} instead.")
            continue

        (id1, corner1), (id2, corner2) = marker_info

        roi_frame = crop_frame(bgr_frame, corner1[0], corner2[0])
        cv2.imshow("Test", roi_frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(0.01)
