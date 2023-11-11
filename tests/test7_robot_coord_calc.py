import sys

sys.path.append("..")
sys.path.append(".")

import time
from pymycobot import MyCobot
from core.config import *
from core.coord_calc import CoordCalc
from core.arm_controls import init_arm

if __name__ == "__main__":
    mc = MyCobot("COM6")
    init_arm(mc)
    print("Init complete.")

    coord_calc = CoordCalc(
        target_base_pos3d, plane_center_pos2d, plane_frame_size_ratio
    )
    test_point = (512 // 2, 512 // 2)
    x, y, z = coord_calc.frame2real(*test_point)
    print(f"Plane center point : {x} {y} {z}")
    print("Please watch if robot move to center of plane.")

    mc.send_angles(arm_pick_hover_angle, 50)
    time.sleep(5)

    x += final_coord_offset[0]
    y += final_coord_offset[1]
    z += final_coord_offset[2]

    coord = [x, y, z] + perpendicular_angle
    mc.send_coords(coord, 50)
    time.sleep(5)
