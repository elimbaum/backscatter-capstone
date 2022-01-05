#!/usr/bin/env python3
#
# receive floats over a UDP socket from gnuradio
#
# TODO: copy over FM0 decoder
# Graphing of magnetic values

import itertools as it
from matplotlib import animation, pyplot as plt
import numpy as np
import socketserver
import struct
import threading
import threading
import time

from enum import Enum
from queue import Queue
from bitarray import bitarray, util as bautil

SYMB_RATE = 2000
SAMP_RATE = 30e3
SPS = SAMP_RATE // SYMB_RATE

# arbitrary for now... 16 is the max
AC_THRESH = 4
ACCESS_CODE = 0xe15ae893
ACCESS_CODE_N_BITS = 32

rawQ = Queue()

class Pulse(Enum):
    SHORT_PULSE  = SPS
    LONG_PULSE   = 2 * SPS
    MID_POINT    = (SHORT_PULSE + LONG_PULSE) // 2
    NOISE_FACTOR = 0.5
    NOISE_PULSE  = SHORT_PULSE * NOISE_FACTOR

class FM0Decoder():
    def unload_queue(self, queue):
        while True:
            yield queue.get()

    # take raw data and return pulse lengths
    def extractPulses(self, raw):
        last = None
        n = 0

        for r in raw:
            # this could become fancy... statistical... etc
            # for now just sign-slice
            b = r > 0
            if b == last:
                n += 1
            else:
                yield n
                last = b
                n = 0

    # handle noise, etc... turn coarse pulses into well defined pulses of the
    # desired length
    def finePulse(self, coarsePulse):
        last = 0
        for b in coarsePulse:
            if b < Pulse.NOISE_PULSE.value:
                last += b + next(coarsePulse)
                continue
            else:
                if last < Pulse.MID_POINT.value:
                    yield Pulse.SHORT_PULSE.value
                else:
                    yield Pulse.LONG_PULSE.value      
            last = b

    # turn pulses into binary symbols
    def pulseToSymbol(self, pulses):
        for p in pulses:
            if p == Pulse.SHORT_PULSE.value:
                if not pulses:
                    break
                
                p = next(pulses)
                if p == Pulse.SHORT_PULSE.value:
                    # short short
                    yield 0
                else:
                    # short long shouldn't happen, so assume error
                    print(".", end='')
                    # yield 0 # is this better?
                    yield 1
            elif p == Pulse.LONG_PULSE.value:
                yield 1

    # take symbols, find packet, return data
    def symbolToPacket(self, symb):
        last_sqn = None
        # convert to binary, and then list. remove "0b" prefix
        access_code_ba = bautil.int2ba(ACCESS_CODE, ACCESS_CODE_N_BITS)

        # store the last `ACCESS_CODE_BITS` symbols to check for the
        # access code. Load with one fewer to get the loop precondition right.
        check_ac = bitarray('0')
        check_ac.extend(it.islice(symb, ACCESS_CODE_N_BITS - 1))

        assert len(check_ac) == ACCESS_CODE_N_BITS

        for s in symb:
            # remove first elm
            del check_ac[0]
            check_ac.append(s)

            # when we see AC, this should be 0
            match = bautil.count_xor(check_ac, access_code_ba)
            
            if match > AC_THRESH:
                print(f"bad ac: {bautil.ba2hex(check_ac)}", end='\r')
                continue

            # good access code, check sqn
            sqn = bautil.ba2int(bitarray(it.islice(symb, 8)))

            if last_sqn is not None and (last_sqn + 1) & 0xFF != sqn:
                print(f"sqn error {bautil.ba2hex(check_ac)} {sqn=:02x}")
                # TODO handle this better.
                # probably should allow sqn sync after some number of
                # sequential errors
                last_sqn = sqn
                yield -np.inf
                continue

            # ok sqn! get len
            last_sqn = sqn

            # this is in bytes
            pkt_len = bautil.ba2int(bitarray(it.islice(symb, 8)))

            # read the data into a byte array
            data_b = bitarray(it.islice(symb, pkt_len * 8)).tobytes()

            # convert to unsigned char
            data = struct.unpack(f"{pkt_len}B", data_b)
            
            # just show a few vals
            partial_str = np.array2string(np.array(data), threshold=0, edgeitems=4)
            print(f"{bautil.ba2hex(check_ac)} {sqn=:02x} {pkt_len=} {partial_str}")

            yield from data

            # have a good correlation!

# create thread for receive/decoding
PLOT_SIZE = 1000
plot_values = np.full((PLOT_SIZE,), -np.inf)

MAX_SENSOR = 239
MIN_SENSOR = 1
SENSOR_ZERO = (MAX_SENSOR + MIN_SENSOR) / 2

def decode_sensor():
    global plot_values
    dec = FM0Decoder()
    
    pulse = dec.extractPulses(dec.unload_queue(rawQ))
    clean_pulse = dec.finePulse(pulse)
    symb = dec.pulseToSymbol(clean_pulse)
    for i, reading in enumerate(dec.symbolToPacket(symb)):
        mapped = (reading - SENSOR_ZERO) / (MAX_SENSOR - SENSOR_ZERO)
        # add to the end and then delete first elm
        plot_values = np.delete(np.append(plot_values, mapped), 0)

##### GRAPHING!

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(-PLOT_SIZE, 0)
ax.set_ylim(-1.1, 1.1)
plt.title("Received Sensor Readings")
plt.ylabel("Magnetism")
plt.xlabel("Time (# of samples ago)")

x = np.arange(-PLOT_SIZE, 0, 1)
plot, = plt.plot(x, plot_values)

AUTOSCALE = True
AUTOSCALE_FACTOR = 1.25

def animate(i):
    plot.set_ydata(plot_values)

    if AUTOSCALE:
        # keep zero in the middle
        max_b = np.where(np.isinf(plot_values), -1, plot_values).max()
        min_b = np.where(np.isinf(plot_values),  1, plot_values).min()

        bound = max(abs(max_b), abs(min_b)) * AUTOSCALE_FACTOR

        # print("bounds", min_b, max_b)
        ax.set_ylim(-bound, bound)

    plt.draw()

    return plot,

anim = animation.FuncAnimation(fig, animate, interval=100)

# Threaded UDP server handles incoming data from GNURadio
# ...eventually the radio stuff could be moved in here, but easier for now.
#
# Note that the main server itself runs in its own thread, but also
# spawns a new thread to handle incoming connections.
class ThreadedUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        req = self.request[0]
        for f in struct.iter_unpack('f', req):
            rawQ.put(f[0])

def run_server():
    HOST, PORT = "127.0.0.1", 5555

    server = socketserver.ThreadingUDPServer((HOST, PORT), ThreadedUDPHandler)
    with server:
        server.serve_forever()

if __name__ == '__main__':
    print("==== Decoder Thread ====")
    decode_thread = threading.Thread(target=decode_sensor, daemon=True)
    decode_thread.start()

    print("==== Server Thread ====")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    print("==== Opening graph... ====")
    plt.show()
