import cv2
import numpy as np
from arm_controls import *
from camera import OrbbecCamera
from config import *
from coord_calc import CoordCalc
from utils import *

coords_transformer = CoordCalc(
    target_base_pos3d,
    (frame_size // 2, frame_size // 2),
    plane_frame_size_ratio,
)

if __name__ == '__main__':
    cam = OrbbecCamera(0)
    aruco_detector = ArucoDetector()

    arm = MyCobot(arm_serial_port)
    init_arm(arm)

    while True:
        if not cam.update_frame():
            time.sleep(frame_interval)
            continue

        color_frame = cam.get_bgr_frame()
        depth_frame = cam.get_depth_frame()

        res = detect_anchor_aruco(color_frame)

        if res is None:
            time.sleep(frame_interval)
            continue

        corner1, corner2 = res
        pt1, pt2 = corner1[0], corner2[0]

        color_frame = crop_frame(color_frame, pt1, pt2)
        depth_frame = crop_frame(depth_frame, pt1, pt2)

        color_frame = cv2.resize(color_frame, (frame_size, frame_size))
        depth_frame = cv2.resize(depth_frame, (frame_size, frame_size))

        visu_frame = visualize_aruco(color_frame)
        cv2.imshow("Preview", visu_frame)

        cv2.waitKey(1)
        time.sleep(frame_interval)

        ids, corners = aruco_detector.detect_marker_corners(color_frame)

        if not (len(ids) != 0 and len(ids) == len(corners)):
            time.sleep(frame_interval)
            continue

        marker_packs = zip(ids, corners)
        marker_packs = list(filter(lambda x: x[0] != 0, marker_packs))

        # Add depth info to marker pack
        new_marker_packs = []
        for m_id, corner in marker_packs:
            m_depth = crop_poly(depth_frame, corner)
            mean_depth = np.sum(m_depth) / np.count_nonzero(m_depth)
            if not np.isnan(mean_depth):
                new_marker_packs.append((m_id, corner, mean_depth))

        marker_packs = new_marker_packs

        # pick the highest marker to grab(lowest in depth)
        marker_pack = min(marker_packs, key=lambda x: x[2])

        m_id, corner, mean_depth = marker_pack
        x, y = np.mean(corner, axis=0)

        x, y, z = coords_transformer.frame2real(x, y)
        z += mean_depth

        grab(arm, x, y, z)


