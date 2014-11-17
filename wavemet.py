from wave import open as wavopen
import pyaudio
import array
import math
import random
import struct

BPM = 120 # Tempo in beats per minute
TIME_SIG = 4 # beats per measure
SEC_PER_BEAT = 60.0/BPM
SAMPLE_LEN = SEC_PER_BEAT*TIME_SIG # Length of the signal in seconds
FRAME_RATE = 44100 # Number of frames per second
FRAME_NUM = SEC_PER_BEAT*44100# Number of frames between each beat
BEAT_SIZE = 0.1*FRAME_RATE # Integer value is number of seconds for a beat
AMP = 10000 # Amplitude of sine wave
_2PI = 2*math.pi
noise_output = wavopen('noise.wav', 'wb')
noise_output.setparams((2, 2, FRAME_RATE, 0, 'NONE', 'not compressed'))

def sine_wave(x):
  return AMP*math.sin(440*_2PI*x/FRAME_RATE) 
  return 0


vals = []
frame_ct = 0
beat_num = 0
while frame_ct < SAMPLE_LEN*FRAME_NUM:
  if frame_ct >= FRAME_NUM*beat_num:
    for i in range(int(BEAT_SIZE)): 
      value = sine_wave(i)
      packed_value = struct.pack('h', value)
      vals.append(packed_value)
      vals.append(packed_value)
      frame_ct+=1
    beat_num+=1
  packed_value = struct.pack('h', 0)
  vals.append(packed_value)
  vals.append(packed_value)
  frame_ct+=1

noise_output.writeframes(''.join(vals))
noise_output.close()

s = wavopen('noise.wav', 'rb')
s.readframes(s.getnframes())
s.close()

print("done writing")
CHUNK = 1024

wf = wavopen('noise.wav','rb')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
channels=wf.getnchannels(),
rate=wf.getframerate(),
output=True)

data = wf.readframes(CHUNK)

while data != '':
  stream.write(data)
  data = wf.readframes(CHUNK)
  if data == '':
    wf.rewind()
    data = wf.readframes(CHUNK)

wf.close()
stream.stop_stream()
stream.close()

p.terminate()
