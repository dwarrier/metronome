from wave import open as wavopen
import pyaudio
import array
import math
import random
import struct

FRAME_RATE = 44100 # Number of frames per second

TIME_SIG = 4 # beats per measure as a reference point
BPM = 60 # Tempo in beats per minute
SEC_PER_BEAT = 60.0/BPM
BEAT_SIZE = 0.1*FRAME_RATE # Integer value is number of seconds for a beat
TOTAL_FRAMES = SEC_PER_BEAT*TIME_SIG*FRAME_RATE # total number of frames for a measure
CHUNK = 1024

AMP = 10000 # Amplitude of sine wave
_2PI = 2*math.pi

def build_values(bpme, freq):
  frame_num = TOTAL_FRAMES/bpme
  vals = []
  frame_ct = 0
  beat_num = 0
  while frame_ct < TOTAL_FRAMES:
    if frame_ct >= frame_num*beat_num:
      for i in range(int(BEAT_SIZE)): 
	value = sine_wave(i,freq)
	packed_value = struct.pack('h', value)
	vals.append(packed_value)
	frame_ct+=1
      beat_num+=1
    packed_value = struct.pack('h', 0)
    vals.append(packed_value)
    frame_ct+=1
  return vals

def sine_wave(x,freq=440):
  return AMP*math.sin(freq*_2PI*x/FRAME_RATE) 
  return 0

noise_output = wavopen('noise.wav', 'wb')
noise_output.setparams((2, 2, FRAME_RATE, 0, 'NONE', 'not compressed'))

a = build_values(3,440)
b = build_values(5,660)
v = [j for i in zip(a,b) for j in i]
noise_output.writeframes(''.join(v))
noise_output.close()

s = wavopen('noise.wav', 'rb')
s.readframes(s.getnframes())
s.close()

print("done writing")

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
