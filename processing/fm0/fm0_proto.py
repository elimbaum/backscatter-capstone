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
import numpy as np
from bitarray import bitarray, util as bautil
import time

SYMB_RATE = 1000
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
        check_ac.extend(itertools.islice(symb, ACCESS_CODE_N_BITS - 1))

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
            sqn = bautil.ba2int(bitarray(itertools.islice(symb, 8)))

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
            pkt_len = bautil.ba2int(bitarray(itertools.islice(symb, 8)))

            # read the data into a byte array
            data_b = bitarray(itertools.islice(symb, pkt_len * 8)).tobytes()

            # convert to unsigned char
            data = struct.unpack(f"{pkt_len}B", data_b)

            print(f"{bautil.ba2hex(check_ac)} {sqn=:02x} {pkt_len=} {data[:4]}")

            yield from data

            # have a good correlation!



def decode_sensor():
    dec = FM0Decoder()
    
    pulse = dec.extractPulses(dec.unload_queue(rawQ))
    clean_pulse = dec.finePulse(pulse)
    symb = dec.pulseToSymbol(clean_pulse)
    for reading in dec.symbolToPacket(symb):
        pass
        # # print(reading, end=', ')
        # if np.isinf(reading):
        #     print()
        # else:
        #     print(reading, "=" * round(reading / 2))


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