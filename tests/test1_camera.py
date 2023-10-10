import sys
import time
import cv2

sys.path.append("..")
sys.path.append(".")

from core.camera import OrbbecCamera


cam = OrbbecCamera(0)

while True:
    if cam.update_frame():
        bgr_frame = cam.get_bgr_frame()
        depth_frame = cam.get_depth_frame()
        depth_frame = cv2.normalize(
            depth_frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1
        )
        depth_frame = cv2.applyColorMap(depth_frame, cv2.COLORMAP_JET)
        cv2.imshow("BGR Frame", bgr_frame)
        cv2.imshow("Depth Frame", depth_frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(0.01)
