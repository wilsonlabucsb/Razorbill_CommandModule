import time
import pickle
import os
import glob

import numpy as np
import argparse

from dataclasses import dataclass
from QDInst import QDInstrument
from pyvisa import ResourceManager

parser = argparse.ArgumentParser(description = "arguement parsing:")
parser.add_argument('--nul', type = float, default = 0)

parser.add_argument('--FIELDS', type = float, nargs='*', required = False)
parser.add_argument('--VAS', type = float, nargs='*', required = False)
parser.add_argument('--VBS', type = float, nargs='*', required = False)
parser.add_argument('--TEMP', type = float, nargs=3, required = False)
parser.add_argument('--QD_FILES', type=pathlib.Path, required = False)

args = parser.parse_args()

print("This will run temperature sweeps at a list of given Fields for each Razorbill Power Setting VAS,VBS supplied:")
                  
if args.FIELDS is None:
    args.FIELDS = input("Range of temperatures in Kelvin: ex. 50 10 2 :  ")
    args.FIELDS = args.FIELDS
if args.VAS is None:
    args.VAS = input("Voltages on CH1 Tension (see temperature dependant limitations in Razorbill User Guide): ex. 0 5 20 50 :  ")
    args.VAS = np.array(args.VAS)
if args.VBS is None:
    args.VBS = input("Voltages on CH2 Compression(see temperature dependant limitations in Razorbill User Guide): ex. 10 10 10 10 :  ")
    args.VBS = np.array(args.VBS)
if args.TEMP is None:
    args.TEMP = input("starting temp (K), end temp (K), ramping rate (K/min): ex. 1.8 300 1:  ")
    args.TEMP = np.array(args.TEMP)
if args.QD_FILES is None:
    args.QD_FILES  = input("Folder Path:  ")
    args.QD_FILES = str(args.QD_FILES)


QD_FILE = max(glob.glob(args.QD_FILES+"*.dat"), key=os.path.getctime)
print("Using File:", QD_FILE)

VAS = np.array(args.VAS)
VBS = np.array(args.VBS)

assert len(VAS) == len(VBS)

rm = ResourceManager()

#use check resources to confirm the port ID of each intrument (USB port ID for the Razorbill ~sparky~ is likely to change)
try:
    sparky_port = "ASRL11::INSTR"
    andy_port = "GPIB0::28::INSTR"
except:
    try:
        sparky_port = "ASRL8::INSTR"
        andy_port = "GPIB0::28::INSTR"
    except:
        print("check address of COMS ports and rewrite the script with correct ports")

def withinpercent(a, b, p = 1):
    if int(a) == 0 or int(b) == 0:
        if int(a) == int(b):
            return True
    elif a / b < (1 + p / 100) and a / b > (1 - p / 100):
        return True
    return False

class Sparky:
    def __init__(self, rm, label=sparky_port):
        self.sparky = rm.open_resource(label)
        # Store a reference to the resource manager so this gets dropped first
        self.__rm = rm

    @property
    def ch1(self):
        return float(self.sparky.query("sour1:volt?"))

    @property
    def ch2(self):
        return float(self.sparky.query("sour2:volt?"))

    @ch1.setter
    def ch1(self, voltage):
        self.sparky.write("outp1 1")
        self.sparky.write("sour1:volt {:f}".format(voltage))

    @ch2.setter
    def ch2(self, voltage):
        self.sparky.write("outp2 1")
        self.sparky.write("sour2:volt {:f}".format(voltage))
    
    def ch1_ramp(self, voltage):
        for v in np.arange(self.ch1, voltage, 0.1):
            self.ch1 = v
        self.ch1 = voltage
    
    def ch2_ramp(self, voltage):
        for v in np.arange(self.ch2, voltage, 0.1):
            self.ch2 = v
        self.ch2 = voltage

    def __del__(self):
        """
        Grounds the outputs when the program ends
        """
        self.sparky.write("sour1:volt 0")
        self.sparky.write("outp1 0")
        self.sparky.write("sour2:volt 0")
        self.sparky.write("outp2 0")

#capacitance bridge
class Andy:
    def __init__(self, rm, label=andy_port):
        self.andy = rm.open_resource(label)
        self.__rm = rm

    def capacitance_string(self):
        return self.andy.query("FETCH")


class QDButNotAwful:
    def __init__(self, tramp_max = 10, framp_max=220, tsleep=0.5, fsleep=0.5):
        self.tramp_max = tramp_max
        self.framp_max = framp_max
        self.tsleep = tsleep
        self.fsleep = fsleep
        self.qd = QDInstrument()

    def set_temp(self, t):
        self.qd.set.temp(t, self.tramp_max, 0)

    def get_temp(self):
        return self.qd.temp
        
    def wait_temp(self, t):
        self.set_temp(t)
        while True:
            time.sleep(self.tsleep)
            if withinpercent(t, self.get_temp()) and self.qd.temp_status == "Stable":
                break

    def ramp_temp(self, start, stop, rate):
        self.wait_temp(start)
        self.qd.set.temp(stop, rate, 0)
        while True:
            time.sleep(self.fsleep)
            if self.qd.temp_status in ["Tracking", "Chasing"]:
                break
    def rampT_complete(self):
        return self.qd.temp_status in ["Stable", "Near"]
        
    def set_field(self, f):
        self.qd.set.field(f, self.framp_max, 0, 1)
        
    def zero_field(self):
        self.wait_field(self.get_field()/10)
        self.qd.set.field(0, self.framp_max, 2, 1)
        while True:
            time.sleep(self.tsleep)
            if withinpercent(0, self.get_field()) and self.qd.field_status in ["Stable", "Holding (Driven)"]:
                break
        
    def get_field(self):
        return self.qd.field

    def ramp_field(self, start, stop, rate):
        self.wait_field(start)
        self.qd.set.field(stop, rate, 0, 1)
        while True:
            time.sleep(self.fsleep)
            if self.qd.field_status in ["Ramping"]:
                break

    def ramp_complete(self):
        return self.qd.field_status in ["Stable", "Holding (Driven)"]

    def wait_field(self, f):
        self.set_field(f)
        while True:
            time.sleep(self.fsleep)
            if withinpercent(f, self.get_field()) and self.qd.field_status in ["Stable", "Holding (Driven)"]:
                break


qd = QDButNotAwful(tramp_max=10)

sparky = Sparky(rm)
andy = Andy(rm)


@dataclass
class Measurement:
    temp: float
    voltages: tuple[float, float]
    field: float
    capstring: str
    qdline: tuple[str, int]


measurments = []

#intitiate starting sequence
sparky.ch1_ramp(0)
sparky.ch2_ramp(10)
qd.zero_field()
qd.wait_temp(args.TEMP[0])

#measure for each condition
for va, vb in zip(VAS, VBS):
    sparky.ch1_ramp(va)
    sparky.ch2_ramp(vb)
    
    for field in args.FIELDS:
        qd.wait_field(field)
        pickle.dump((measurments, open(QD_FILE, "r").read()) , open("backup-{:f}.pkl".format(time.time()), "wb"))
        qd.ramp_temp(*args.TEMP)
        
        while not qd.rampT_complete():
            lines = open(QD_FILE, 'r').readlines()
            measurments.append(
                Measurment(
                    qd.get_temp(),
                    (va, vb),
                    field,
                    andy.capacitance_string(),
                    (lines[-1], len(lines))
                )
            )
            print(measurments[-1])
        
#output data file
pickle.dump((measurments, open(QD_FILE, "r").read()) , open("mymeasurements-{:f}.pkl".format(time.time()), "wb"))

#outro sequence
sparky.ch1_ramp(0)
sparky.ch2_ramp(0)
qd.zero_field()
qd.wait_temp(300)

#### END ####
