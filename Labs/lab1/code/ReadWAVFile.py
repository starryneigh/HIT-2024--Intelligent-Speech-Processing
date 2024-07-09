# -*- coding: utf-8 -*-

import wave
import numpy as np
import struct


class rff(object):
    'Read from file'

    def __init__(self, filename):

        try:
            file = wave.open(filename, 'rb')
        except FileNotFoundError as e:
            print('Exception', e)
        else:
            parameters = file.getparams()
            self._nchannels, self._sampwidth, self._framerate, self._nframes = parameters[:4]
            self._str_data = file.readframes(self._nframes)
            self._wave_data = np.fromstring(self._str_data, dtype=np.short)
            self._data_size = len(self._wave_data)

    def getFrameListData(self):
        return self._wave_data

    def getFrameData(self):
        return self._nframes

    def getNchannel(self):
        return self._nchannels

    def getSampwidth(self):
        return self._sampwidth

    def getFrameRate(self):
        return self._framerate

    def getRawData(self):
        return self._nchannels, self._sampwidth, self._framerate, self._nframes


class wtf(object):
    'Write to file'

    def __init__(self, filename, data):
        self._data = data
        self._write_file(filename)

    def _write_file(self, filename):
        data = self._data
        file_data = open(filename, 'wb+')
        size_data = len(data)

        for i in range(size_data):
            a = int(data[i])
            a = struct.pack('h', int(a))
            file_data.write(a)
