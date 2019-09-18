import json
import deepmerge
import time
import sys
import serial

merge = deepmerge.Merger([(dict, ["merge"])], ["override"], ["override"]).merge

default_config = {
    "serial": {"port": "/dev/ttyUSB0", "baudrate": 115200}
}

config = merge(default_config, json.loads(sys.argv[1]))

with serial.Serial(timeout=2.0, **config["serial"]) as ser:
     while True:
          line = ser.readline()
          if not line.startswith(b"$status"):
               ser.write(b"status -stream\n")
               continue
          line = line.split(b"=")[1]
          line = [float(item) for item in line.split(b",")]
          
          json.dump({
               "engine": {"left": line[1], "right": line[2]},
               "time_engine": line[0],
               "time": time.time()}, sys.stdout)
          sys.stdout.write("\n")
          sys.stdout.flush()
