from typing import Tuple, Union
import numpy as np
import cv2
from aruco_detector import ArucoDetector


def crop_frame(frame: np.ndarray, pt1: Tuple[int, int], pt2: Tuple[int, int]):
    x1, y1 = pt1
    x2, y2 = pt2
    if x1 > x2 and y1 > y2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    frame_local = frame.copy()
    return frame_local[y1: y2, x1: x2]


def crop_poly(frame: np.ndarray, ploy_vertices: np.ndarray) -> np.ndarray:
    mask = np.zeros(frame.shape, dtype=np.uint8)
    ploy_vertices = ploy_vertices.reshape((-1, 1, 2))
    ploy_vertices = ploy_vertices.astype(np.int32)
    cv2.fillPoly(mask, [ploy_vertices], 255)
    polygon_region = cv2.bitwise_and(frame, frame, mask=mask)
    return polygon_region


def detect_anchor_aruco(frame) -> Union[Tuple[np.ndarray, np.ndarray], None]:
    aruco_detector = ArucoDetector()
    ids, corners = aruco_detector.detect_marker_corners(frame)
    if len(ids) == 0 and len(corners) == 0:
        print("No aruco found.")
        return None

    corners = corners.astype(np.int32)
    marker_info = zip(ids, corners)
    marker_info = list(filter(lambda x: x[0] == 0, marker_info))
    if len(marker_info) != 2:
        print(f"Anchor point error, should have 2 anchor points, got {len(marker_info)} instead.")
        return None

    (id1, corner1), (id2, corner2) = marker_info

    return corner1, corner2


def visualize_aruco(frame):
    aruco_detector = ArucoDetector()
    ids, corners = aruco_detector.detect_marker_corners(frame)
    visu_frame = aruco_detector.visualize(frame, ids, corners)
    return visu_frame
