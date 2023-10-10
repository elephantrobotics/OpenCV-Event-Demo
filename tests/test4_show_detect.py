import sys
sys.path.append("..")
sys.path.append(".")

from core.camera import OrbbecCamera
from core.utils import crop_frame
from core.aruco_detector import ArucoDetector
import cv2
import time
import numpy as np

cam = OrbbecCamera(0)
aruco_detector = ArucoDetector()

while True:
    if cam.update_frame():
        bgr_frame = cam.get_bgr_frame()
        depth_frame = cam.get_depth_frame()
        depth_frame = cv2.normalize(depth_frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        depth_frame = cv2.applyColorMap(depth_frame, cv2.COLORMAP_JET)

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

        roi_color_frame = crop_frame(bgr_frame, corner1[0], corner2[0])
        roi_depth_frame = crop_frame(depth_frame, corner1[0], corner2[0])

        ids, corners = aruco_detector.detect_marker_corners(roi_color_frame)
        visu_frame = aruco_detector.visualize(roi_color_frame, ids, corners)

        cv2.imshow("Color", visu_frame)
        cv2.imshow("Depth", roi_depth_frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(0.01)
