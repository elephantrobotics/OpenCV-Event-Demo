import sys
import time

sys.path.append("..")
sys.path.append(".")

from core.utils import *
from pymycobot import  MyCobot
from core.config import arm_serial_port
from core.arm_controls import pump_on, pump_off

arm = MyCobot(arm_serial_port)

pump_on(arm)
time.sleep(3)

pump_off(arm)
time.sleep(3)