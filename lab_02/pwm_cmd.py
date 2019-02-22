# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 19:53:28 2019

@author: Adib Yahaya
"""

import sys
import argparse
import time
import mmap
import struct

def Enable(arg):
    # open dev mem and see to base address
    f = open("/dev/mem", "r+b")
    mem = mmap.mmap(f.fileno(), 32, offset=0x43c10000)
    
    # Enable the PWM
    toEnable = int(arg)
    reg = 0

    mem.seek(reg)  
    mem.write(struct.pack('l', toEnable))

    time.sleep(.5) 

    mem.seek(reg)  
    fromMem = struct.unpack('l', mem.read(4))[0] 
  
    print str(reg) + " = " + str(fromMem) 
    # Close mem after finishing
    mem.close()
    f.close()

def Period(arg):
    # open dev mem and see to base address
    f = open("/dev/mem", "r+b")
    mem = mmap.mmap(f.fileno(), 32, offset=0x43c10000)
    
    # Set the  period

    toPeriod = int(arg)
    reg = 4

    mem.seek(reg)  
    mem.write(struct.pack('l', toPeriod))

    time.sleep(.5) 

    mem.seek(reg)  
    fromMem = struct.unpack('l', mem.read(4))[0] 

    print str(reg) + " = " + str(fromMem)
    # Close mem after finishing
    mem.close()
    f.close()

def DutyCycle(arg):
    # open dev mem and see to base address
    f = open("/dev/mem", "r+b")
    mem = mmap.mmap(f.fileno(), 32, offset=0x43c10000)
    
    # Set the  duty cycle

    toDutyCycle = int(arg)
    reg = 8

    mem.seek(reg)  
    mem.write(struct.pack('l', toDutyCycle))

    time.sleep(.5) 

    mem.seek(reg)  
    fromMem = struct.unpack('l', mem.read(4))[0] 

    print str(reg) + " = " + str(fromMem)
    # Close mem after finishing
    mem.close()
    f.close()


def main(argv):
    parser = argparse.ArgumentParser(description='Set PWM parameters')
    parser.add_argument('enable', type=int, help='0/1 to disable or enable')
    parser.add_argument('period', type=int, help='Set the PWM frequency')
    parser.add_argument('dutyCycle', type=int, help='Set the duty cycle')
    args = parser.parse_args()
    
    Enable(args.enable)
    Period(args.period)
    DutyCycle(args.dutyCycle)

        
if __name__ == "__main__":
    main(sys.argv[1:])
