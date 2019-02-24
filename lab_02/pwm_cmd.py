import sys
import argparse
import time
import mmap
import struct

def WriteToMem(val, reg):
    # open dev mem and see to base address
    f = open("/dev/mem", "r+b")
    mem = mmap.mmap(f.fileno(), 32, offset=0x43c10000)

    toMem = int(val)

    mem.seek(reg)
    mem.write(struct.pack('l', toMem))

    time.sleep(.5)

    mem.seek(reg)
    fromMem = struct.unpack('l', mem.read(4))[0]

    print str(reg) + " = " + str(fromMem)
    # Close mem after finishing
    mem.close()
    f.close()

    if (int(val) == int(fromMem)):
        result = 1
    else:
        result = 0
        print "Failed to write to mem"

    return result

def main(argv):
    # To directly run this script with CLI
    parser = argparse.ArgumentParser(description='Set PWM parameters')
    parser.add_argument('enable', type=int, help='0/1 to disable or enable')
    parser.add_argument('period', type=int, help='Set the PWM frequency')
    parser.add_argument('dutyCycle', type=int, help='Set the duty cycle')
    args = parser.parse_args()

    # Enable: reg = 0
    # Period: reg = 4
    # Duty Cycle: reg = 8
    WriteToMem(args.enable, 0)
    WriteToMem(args.period, 4)
    WriteToMem(args.dutyCycle, 8)

if __name__ == "__main__":
    main(sys.argv[1:])