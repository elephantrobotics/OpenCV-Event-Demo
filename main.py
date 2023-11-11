import sys
from core.arm_controls import *
from core.camera import OrbbecCamera
from core.config import *
from core.coord_calc import CoordCalc
from core.utils import *

coords_transformer = CoordCalc(
    target_base_pos3d,
    (frame_size // 2, frame_size // 2),
    plane_frame_size_ratio,
)

if __name__ == "__main__":
    cam = OrbbecCamera(0)
    aruco_detector = ArucoDetector()
    logger = get_logger(__name__)

    print("Press Q/q to exit.")

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
            logger.warning(f"anchor aruco not detected. try again next frame.")
            time.sleep(frame_interval)
            continue

        # preprocess frame
        corner0, corner1 = res

        color_frame = crop_frame_by_anchor(color_frame, corner0, corner1)
        depth_frame = crop_frame_by_anchor(depth_frame, corner0, corner1)

        color_frame = cv2.resize(color_frame, (frame_size, frame_size))
        depth_frame = cv2.resize(depth_frame, (frame_size, frame_size))

        visu_frame = visualize_aruco(color_frame)
        cv2.imshow("Preview", visu_frame)

        key = cv2.waitKey(1)

        if cv2.waitKey(1) in [ord("q"), ord("Q")]:
            print("Bey.")
            cam.release()
            sys.exit(0)

        ids, corners = aruco_detector.detect_marker_corners(color_frame)

        if not (len(ids) != 0 and len(ids) == len(corners)):
            logger.info(
                "Not detecting any aruco marker within the zone. try again next frame."
            )
            time.sleep(frame_interval)
            continue

        # pack id and corners together
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

        # extract marker pack; translate frame pos to real world pos.
        m_id, corner, mean_depth = marker_pack
        x, y = np.mean(corner, axis=0)

        x, y, z = coords_transformer.frame2real(x, y)
        z += floor_depth - mean_depth

        x += final_coord_offset[0]
        y += final_coord_offset[1]
        z += final_coord_offset[2]

        logger.info(f"Target position: {x},{y},{z}")

        grab(arm, x, y, z)
