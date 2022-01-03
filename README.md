# Low-power Backscatter Communications

*NSAP Capstone Project, 2021*

Eli Baum

- topic sentences
- active voice

## Overview

Standard radio communications systems require significant power and ... large size ... //

Backscatter technology allows for one-way communication without such large, power-hungry components. Rather than generating its own radio signals, a backscatter system modulates reflected radio signals from another source.

Since the sensor system is effectively doing nothing more than switching a transistor at a given frequency, it requires little power. Past academic research has even demonstrated the ability for relatively complex backscatter systems to be powered entirely by harvested ambient radio frequency energy.

Due to its low power requirements and simple operations, backscatter systems can be manufactured cheaply and therefore provide distributed sensing capabilities. ## who ## could distribute thousands of sensors across an area of interest, occasionally collecting 

In this prototype, an SDR is used to generate a fixed-frequency tone at 915 MHz. The sensor modulates data at approximately 150 kHz; the receive side of the SDR is therefore tuned to 915.15 MHz.

## Backscatter

Backscatter communication can seem counterintuitive compared to standard wireless communication systems. The following analogy may help clarify its operation:

Consider two parties, Alice and Bob, who wish to communicate with each other using light. (For the purposes of argument, assume there is a line of sight between them, and that it is nighttime.) The simplest method for Alice to send a message would probably be for her to point a flashlight at Bob and turn it on and off under some modulation scheme (say, Morse code). Bob could record Alice's pulses of light and translate them into a message. Bob could then reply with the same method.

However, there are several drawbacks to this system. Both Alice and Bob must, of course, carry flashlights, which may be heavy, require large power supplies, and generate significant heat. Additionally, if Alice would like to communicate covertly (or are trying to hide their locations), a flashlight might be too easy for their adversary, Eve, to detect.

> If we were actually discussing optical communication, one might suggests lasers to decrease detectability, but since this is an analogy for radio communications, lasers will not be of much use.

Alice comes up with an alternative scheme: she carries a mirror which she uses to carefully reflect moonlight in Bob's direction. The resulting light will be much dimmer, from Bob's perspective, but Alice no longer needs to carry a flashlight. 

Alice and Bob soon run into an issue - if the moon is not in the sky, or it is cloudy, they are unable to communicate. Seeking more reliable communication, Bob sets up a lantern near his location; Alice can once again either reflect, or not reflect, the light from the lantern towards Bob.

One problem remains: how can Bob see Alice's dim reflections, when the lantern is so bright (and likely much closer)? Besides taking advantage of the directionality of shades and lenses, Bob may have quite a hard time distinguishing Alice's signal from the background noise. However, imagine a *phosphorescent mirror*, one which changes the color of reflected light. Then, Bob could filter the wavelength of light coming from his lantern; only Alice's signal will remain.

---

Many of the concepts and compromises discussed above apply to radio communications, as well. The final scenario - where Bob illuminates Alice's color-changing reflector, and detects the return signal - closely mirrors how backscatter *radio* communications works.

In this prototype, we use an SDR as both illuminator and detector. The transmit (TX) end of the SDR broadcasts a constant-frequency cosine tone; this is similar to Bob's lantern. The analog of the tilting mirror is the antenna mounted on the sensor module, which is connected through an RF switch to a 50Ω termination. When the switch is open, and the antenna acts like a mirror. When the switch is *closed*, signals are attenuated by the terminator - we have, in essence, an electrically-controlled radio mirror.

For the "color-changing" component of Alice's mirror, we take advantage of *beat frequencies*.

Recall that for two signals $A$ and $B$, with respective frequencies $f_A$ and $f_B$, the addition of those two signals $A+B$ will appear to have a frequency component at $f_A \pm f_B$. This is often noted in the context of musical instruments, where it can be used to tune notes, but we can just as easily use it to create a frequency-shifting effect. In our prototype, the cosine illuminator is transmitted at 915 MHz ($=f_A$); the sensor module is configured to toggle the RF switch at approximately 150 kHz ($=f_A$). Therefore, we expect artifacts to appear at $915\pm0.15$ MHz. By tuning the receive (RX) side of the SDR, therefore, to 915.15 MHz, and keeping its bandwidth below 300 kHz, we entirely eliminate interfere from the transmitter.

At this point the reflected signal can be modulated in various ways. See *[Physical Layer](#physical-layer)*, below, for further details.

### A Word on Radar

ambient: discuss NRL, TV towers, bistatic

### A Word on RFID

Passive - magnetic induction
Active - interrogator with a transmitter

## Prototype Components

### Physical Layer

#### Amplitude Shift Keying

We use amplitude-shift keying (ASK) to modulate data; this is the simplest scheme that could be used for the purposes of a viable prototype. 

We experimented with frequency-shift keying (FSK) but decided not to implement it fully; FSK provides superior information density but is less noise-tolerant and more computationally complex to decode. Furthermore, the usefulness of an FSK system was limited by the granularity of the microcontroller's internal oscillator.

Other schemes, such as phase-shift keying (PSK) and quadrature amplitude modulation (QAM) were not possible with the hardware available on the sensor module. The RF switch contained a purely resistive internal load; phase-related modulations would be possible with reactive (i.e. capacitive) loads. A fieldable backscatter solution would require more advanced hardware capable of these advanced modulation schemes.

#### FM0

Once we are able to modulate the signal, the next problem is to actually send bits. In particular, we need a *clock recovery* method - how do we align our receiver with our reflector? In this prototype, we have used *FM0 encoding*, an extremely simple run-length limited (RLL) code. RLL codes are designed to have enough transitions int the transmitted signal to enable clock recovery; without FM0, a string of identical values could be difficult to decode.

In fact, FM0 is quite similar to Morse code. `1` bits are encoded as a long pulse, while `0` is encoded as two short pulses (hence the "FM" or "frequency modulation" in its name). We do not care about the actual level of these pulses, but only their *transitions*: after every bit, we toggle the signal, but for a `0`, we also toggle within that bit period. For example, to send the data `0110`, we encode:

    Data:   | 0| 1| 1| 0|
    TX: ...0 10 11 00 10 1...
    Pulses:  SS  L  L SS

While this is not particularly efficient (it takes 2 symbols to send one bit), it is simple to implement and appropriate for prototyping.

At this point, a fieldable system should also include error-detection and correction schemes to ensure reliable communication at a distance. We implemented a Hamming encoder and decoder, but for simplicity's sake, did not include it in the final prototype.

### Packet Layer

Various data-transmission strategies are possible; we chose continuous data transmission, since this is simple and beneficial for demonstration purposes. We designed a packet format, as follows:

    Access Code [32 bits]
        0x e1 5a e8 93
    Sequence number [8 bits]
        xx
    Data Length, bytes [8 bits]
        xx
    Data (8 bits per reading)
        ...

The access code, `0xe15ae893` is a commonly-used access code with strong auto-correlation properties. This makes it easy for the decoder to synchronize to the start of the packet: the access code correlates poorly with itself at all offsets except 0.

The sequence number provides some level of error detection, however - it is incremented for each packet (overflowing from 255 to 0); the decoder only accepts a packet if the decoded sequence number is one greater than the previous.

### Sensor Demonstration

The focus of this project was on backscatter communication itself, not on the particular data sent over the backscatter link. Here, we add a magnetic sensor to the backscatter sensor, to demonstrate real-time communication capabilities. We take a moving average of the sensor readings and send 16 8-bit values per packet.

With these parameters, each packet is therefore 176 bits. At a symbol rate of 2000 baud, we can send 1000 bits per second. This gives about 5.7 packets per second, or 91 readings per second.

## Decoder Implementation

The Python decoder is implemented as a series of layers:

1. SDR samples decoded into ASK symbols
2. Pulse length determination
3. Pulse length clustering - determination of *short* or *long* pulse
4. FM0 decoding - convert pulses to symbols  
5. Packet decoding
6. Data graphing

## Caveats and Future Work