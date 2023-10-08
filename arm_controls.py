import time
from pymycobot import MyCobot
import platform
from config import *


def init_arm(arm: MyCobot):
    arm.send_angles(arm_idle_angle, 50)
    arm.set_fresh_mode(0)
    time.sleep(1)
    arm.set_tool_reference(tool_frame)
    time.sleep(1)
    arm.set_end_type(1)
    time.sleep(1)
    pump_off(arm)
    time.sleep(3)


def grab(arm: MyCobot, x, y, z):
    # hover to avoid collision
    arm.send_angles(arm_pick_hover_angle, 50)
    time.sleep(3)

    coord = [x, y, z]

    # make arm perpendicular to the plane
    coord.extend([177, 0, 90])

    # move x-y first, set z fixed
    target_xy_pos3d = coord.copy()[:3]
    target_xy_pos3d[2] = 80

    print(f"X-Y move: {target_xy_pos3d}")
    position_move(arm, *target_xy_pos3d)
    time.sleep(3)

    # send target angle
    print(f"Target move: {coord}")
    arm.send_coords(coord, 50)
    time.sleep(3)

    pump_on(arm)
    time.sleep(1)

    arm.send_angles(arm_drop_angle, 50)
    time.sleep(3)

    pump_off(arm)
    time.sleep(1)

    arm.send_angles(arm_idle_angle, 50)
    time.sleep(3)


def pump_on(arm: MyCobot):
    if platform.system() == "Windows":
        arm.set_basic_output(5, 0)
        time.sleep(0.05)
    elif platform.system() == "Linux":
        # TODO
        pass


def pump_off(arm: MyCobot):
    if platform.system() == "Windows":
        arm.set_basic_output(5, 1)
        time.sleep(0.05)
        # 泄气阀门开始工作
        arm.set_basic_output(2, 0)
        time.sleep(1)
        arm.set_basic_output(2, 1)
        time.sleep(0.05)
    elif platform.system() == "Linux":
        # TODO
        pass


def position_move(arm: MyCobot, x, y, z):
    curr_rotation = arm.get_coords()[-3:]
    curr_rotation[0] = 175
    curr_rotation[1] = 0
    target_coord = [x, y, z]
    target_coord.extend(curr_rotation)
    print(f"Move to coords : {target_coord}")
    arm.send_coords(target_coord, 50)
