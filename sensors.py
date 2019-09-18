import time
import hmc5883l
import mpu6050
import json
import deepmerge
import sys

merge = deepmerge.Merger([(dict, ["merge"])], ["override"], ["override"]).merge

default_config = {
    "accel": {"bus": 0, "address": 0x68},
    "compass": {"gauss": 4.7, "declination": (-2,5), "port": 0},
    "frequency": 100
}

config = merge(default_config, json.loads(sys.argv[1]))

accel = mpu6050.mpu6050(**config["accel"])
compass = hmc5883l.hmc5883l(**config["compass"])

while True:
    json.dump({
        "accel": accel.get_accel_data(),
        "gyro": accel.get_gyro_data(),
        "temp": accel.get_temp(),
        "heading": compass.heading(),
        "time": time.time()}, sys.stdout)
    sys.stdout.write("\n")
    sys.stdout.flush()
    time.sleep(1./config["frequency"])
