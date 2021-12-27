#!/usr/bin/env python3
#
# receive floats over a UDP socket from gnuradio
#
# TODO: copy over FM0 decoder
# Graphing of magnetic values

import socketserver
import struct
import itertools
from queue import Queue
from enum import Enum
import threading

SYMB_RATE = 1000
SAMP_RATE = 30e3
SPS = SAMP_RATE / SYMB_RATE

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

    # this could become fancy
    def slicer(self, raw):
        for r in raw:
            yield r > 0

    def coarsePulse(self, bits):

    def finePulse(self, coarse):
        last = 0
        for b in coarse:
            if b < Pulse.NOISE_PULSE.value:
                last += b + next(bits)
                continue
            else:
                if last < Pulse.MID_POINT.value:
                    yield Pulse.SHORT_PULSE.value
                else:
                    yield Pulse.LONG_PULSE.value      
        last = b

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
                    print("sync")
                    yield 1
            elif p == Pulse.LONG_PULSE.value:
                yield 1

def decode_sensor():
    dec = FM0Decoder()
    
    bin = dec.slicer(dec.unload_queue(rawQ))
    pulse = dec.binToPulse(bin)
    symb = dec.pulseToSymbol(pulse)

    for q in symb:
        print(q)


class ThreadedUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        req = self.request[0]
        for f in struct.iter_unpack('f', req):
            rawQ.put(f[0])

if __name__ == '__main__':
    HOST, PORT = "localhost", 5555

    decode_thread = threading.Thread(target=decode_sensor, daemon=True)
    decode_thread.start()

    server = socketserver.ThreadingUDPServer((HOST, PORT), ThreadedUDPHandler)
    with server:
        print("Starting server...")
        server.serve_forever()