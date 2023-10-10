import sys
sys.path.append("..")
sys.path.append(".")

from core.camera import OrbbecCamera
from core.utils import *
import cv2
import time
import numpy as np
from typing import *

cam = OrbbecCamera(0)
aruco_detector = ArucoDetector()

while True:
    if cam.update_frame():
        bgr_frame = cam.get_bgr_frame()
        depth_frame = cam.get_depth_frame()

        ids, corners = aruco_detector.detect_marker_corners(bgr_frame)

        if len(ids) == 0 and len(corners) == 0:
            print("No aruco found.")
            continue

        corners = corners.astype(np.int32)

        # get anchor aruco marker
        marker_info = zip(ids, corners)
        marker_info = list(filter(lambda x: x[0] == 0, marker_info))
        if len(marker_info) != 2:
            print(f"anchor point error, should have 2 anchor points, got {len(marker_info)} instead.")
            continue

        (id1, corner1), (id2, corner2) = marker_info

        roi_color_frame = crop_frame(bgr_frame, corner1[0], corner2[0])
        roi_depth_frame = crop_frame(depth_frame, corner1[0], corner2[0])

        ids, corners = aruco_detector.detect_marker_corners(roi_color_frame)
        color_visu_frame = aruco_detector.visualize(roi_color_frame, ids, corners)

        marker_packs: List[Tuple[int, np.ndarray, int]] = zip(ids, corners)
        marker_packs = list(filter(lambda x: x[0] != 0, marker_packs))

        if len(marker_packs) == 0:
            print("Don't found any aruco within the zone, try again next frame.")
            time.sleep(0.01)
            continue

        # Add depth info to marker pack
        new_marker_packs = []
        for m_id, corner in marker_packs:
            m_depth = crop_poly(roi_depth_frame, corner)
            divider = np.count_nonzero(m_depth)
            # prevent divided by zero error
            if divider == 0:
                continue

            mean_depth = np.sum(m_depth) / divider
            if not np.isnan(mean_depth):
                new_marker_packs.append((m_id, corner, mean_depth))

        marker_packs = new_marker_packs

        if len(marker_packs) == 0:
            print("Don't found any aruco with valid depth value, try again next frame.")
            time.sleep(0.01)
            continue

        # pick the highest marker to grab(lowest in depth)
        marker_pack: Tuple[int, np.ndarray, int] = min(marker_packs, key=lambda x: x[2])
        m_id, corner, mean_depth = marker_pack
        corner = corner.astype(np.int32)
        cv2.polylines(color_visu_frame, [corner], isClosed=True, color=(255, 255, 0), thickness=1)
        cv2.putText(color_visu_frame, "{:.2f}".format(mean_depth), corner[1], cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                    color=(255, 255, 0), thickness=1)

        depth_visu_frame = cv2.normalize(roi_depth_frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        depth_visu_frame = cv2.applyColorMap(depth_visu_frame, cv2.COLORMAP_JET)

        cv2.imshow("Color", color_visu_frame)
        cv2.imshow("Depth", depth_visu_frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(0.01)
