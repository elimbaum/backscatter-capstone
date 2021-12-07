#!/usr/bin/env python3
# FM0 decoder
#
# GNURadio sends bits over a socket (eventually, put the SDR stuff in here)

import socketserver
from queue import Queue
import threading
import time
from enum import Enum

# expected pulse lengths.
# for now, 30k samp/sec and 1k symb/sec
class Pulse(Enum):
    NOISE_PULSE = 10
    SHORT_PULSE = 30
    LONG_PULSE  = 60
    MID_POINT   = (SHORT_PULSE + LONG_PULSE) // 2

bitQ = Queue()

def read_bits():
    last = None
    n = 0

    while True:
        b = bitQ.get()
        if b == last:
            n += 1
        else:
            yield n
            last = b
            n = 0

def find_pulses():
    # this will return offset by one
    last = 0
    bit_iter = iter(read_bits())
    for p in bit_iter:
        if p < Pulse.NOISE_PULSE.value:
            # print("noise")
            last += p + next(bit_iter)
            continue
        else:
            if last < Pulse.MID_POINT.value:
                yield Pulse.SHORT_PULSE
            else:
                yield Pulse.LONG_PULSE
        last = p

def convert_symbols():
    pulse_iter = iter(find_pulses())
    for p in pulse_iter:
        if p == Pulse.SHORT_PULSE:
            p = next(pulse_iter)
            if p == Pulse.SHORT_PULSE:
                yield 0
            else:
                # print("sync")
                yield 1
        else:
            yield 1

def analysis():
    print("Starting analysis...")

    BLOCK_SIZE = 1000
    n = 0
    correct = 0
    last = None

    for symb in convert_symbols():
        if last is not None and last != symb:
            correct += 1

        if n >= BLOCK_SIZE:
            n = correct = 0

        if n and n % 10 == 0:
            print(f"== {100 * correct / n:.2f}% ==", end='\r')

        n += 1
        last = symb



class ThreadedUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        for b in self.request[0]:
            bitQ.put(b)

if __name__ == '__main__':
    HOST, PORT = "localhost", 5555

    analysis_thread = threading.Thread(target=analysis)
    analysis_thread.daemon = True
    analysis_thread.start()

    server = socketserver.ThreadingUDPServer((HOST, PORT), ThreadedUDPHandler)
    with server:
        print("Starting server...")
        server.serve_forever()