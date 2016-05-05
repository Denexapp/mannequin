"""
by Denexapp

"""

import wave
import numpy as np
import file_io
# import matplotlib.pyplot as plt

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}


def decode_wav(name):
    wav = wave.open(name, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    # duration = nframes / framerate
    #  w, h = 800, 300
    # framerate per time 32000 * 0.01
    k = framerate * 0.01
    DPI = 72
    peak = 256 ** sampwidth / 2

    content = wav.readframes(nframes)
    samples = np.fromstring(content, dtype=types[sampwidth])

    # plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
    result = 0
    for n in range(nchannels):
        channel = samples[n::nchannels]
        channel = channel[0::k]

        z = 0
        for a in channel:
            channel[z] = abs(a)/nchannels
            z+=1

        if n == 0:
            result = np.copy(channel)
            continue
        # if nchannels == 1:
        #     channel = channel - peak
    #result - summ of all channels, 100 fps

    result_2 = np.zeros(result.size/10-1)
    i = 0
    for element in range(result.size/10-1):
        area = np.zeros(10)
        p = 0
        while p < 10:
            half_result = result[i*10+p]
            if half_result > 3500:
                half_result = half_result ** 1.3 - 3500 ** 1.3 - 3500
            area[p] = half_result
            p += 1
        result_2[i] = area.max()
        i += 1
    #result_2 - maxes, 10 fps

    result = np.zeros((result_2.size-1)*10+1)
    for i in range(result_2.size-1):
        start = result_2[i]
        end = result_2[i+1]
        delta = end - start
        start_pos = i*10
        for m in range(10):
            result[start_pos+m] = start + delta * m/10
    result[result.size-1] = result_2[result_2.size-1]
    result = result.tolist()
    # result is smoothed
    # axes = plt.subplot(2, 1, n+1, axisbg="k")
    # axes.plot(result, "g")

    # plt.savefig("wave", dpi=DPI)
    # plt.show()
    return result


def create_markup(filename):
    first = True
    res = ""
    a = decode_wav(filename)
    for element in a:
        if first:
            first = False
        else:
            res = res + " "
        res = res + str(element)
    file_io.write(filename.split(".")[0]+".mp3_markup", res)

if __name__ == "__main__":
    while True:
        name = raw_input('Enter filename\n')
        create_markup(name)
        print "success"
