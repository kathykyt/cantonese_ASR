#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  downsample.py
#  
#  Copyright 2015 John Coppens <john@jcoppens.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#

inwave = "sine_44k.wav"
outwave = "sine_16k.wav"

import wave
import numpy as np
import scipy.signal as sps

class DownSample():
    def __init__(self):
        self.in_rate = 44100.0
        self.out_rate = 16000.0

    def open_file(self, fname):
        try:
            self.in_wav = wave.open(fname)
        except:
            print("Cannot open wav file (%s)" % fname)
            return False

        if self.in_wav.getframerate() != self.in_rate:
            print("Frame rate is not %d (it's %d)" % \
                  (self.in_rate, self.in_wav.getframerate()))
            return False

        self.in_nframes = self.in_wav.getnframes()
        print("Frames: %d" % self.in_wav.getnframes())

        if self.in_wav.getsampwidth() == 1:
            self.nptype = np.uint8
        elif self.in_wav.getsampwidth() == 2:
            self.nptype = np.uint16

        return True

    def resample(self, fname):
        self.out_wav = wave.open(fname, "w")
        self.out_wav.setframerate(self.out_rate)
        self.out_wav.setnchannels(self.in_wav.getnchannels())
        self.out_wav.setsampwidth (self.in_wav.getsampwidth())
        self.out_wav.setnframes(1)

        print("Nr output channels: %d" % self.out_wav.getnchannels())

        audio = self.in_wav.readframes(self.in_nframes)
        nroutsamples = round(len(audio) * self.out_rate/self.in_rate)
        print("Nr output samples: %d" %  nroutsamples)

        audio_out = sps.resample(np.fromstring(audio, self.nptype), nroutsamples)
        audio_out = audio_out.astype(self.nptype)

        self.out_wav.writeframes(audio_out.copy(order='C'))

        self.out_wav.close()

def main():
    ds = DownSample()
    if not ds.open_file(inwave): return 1
    ds.resample(outwave)
    return 0

if __name__ == '__main__':
    main()
