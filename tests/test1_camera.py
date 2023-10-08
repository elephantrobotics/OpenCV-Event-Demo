from camera import OrbbecCamera
import time
import cv2

cam = OrbbecCamera(0)

while True:
    if cam.update_frame():
        bgr_frame = cam.get_bgr_frame()
        depth_frame = cam.get_depth_frame()
        cv2.imshow("BGR Frame", bgr_frame)
        cv2.imshow("Depth Frame", depth_frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(0.01)
