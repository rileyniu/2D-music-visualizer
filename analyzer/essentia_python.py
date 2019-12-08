# This is how the audio we want to process sounds like
import IPython
import numpy
import json 
import essentia
import essentia.standard as es
from essentia.standard import *
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt

pool = essentia.Pool(); 

# Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame features
features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                              rhythmStats=['mean', 'stdev'],
                                              tonalStats=['mean', 'stdev'])('../data/../data/flamenco.wav')

# See all feature names in the pool in a sorted order
print(sorted(features.descriptorNames()))

# You can then access particular values in the pools:
print("Filename:", features['metadata.tags.file_name'])
print("-"*80)
print("Replay gain:", features['metadata.audio_properties.replay_gain'])
print("EBU128 integrated loudness:", features['lowlevel.loudness_ebu128.integrated'])
print("EBU128 loudness range:", features['lowlevel.loudness_ebu128.loudness_range'])
print("-"*80)
print("MFCC mean:", features['lowlevel.mfcc.mean'])
print("-"*80)
print("BPM:", features['rhythm.bpm'])
print("Beat positions (sec.)", features['rhythm.beats_position'])
print("-"*80)
print("Key/scale estimation (using a profile specifically suited for electronic music):",
      features['tonal.key_edma.key'], features['tonal.key_edma.scale'])

# BPM Detection

# Loading audio file
audio = MonoLoader(filename='../data/flamenco.wav')()

# # Compute beat positions and BPM
rhythm_extractor = RhythmExtractor2013(method="multifeature")
bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

# print("BPM:", bpm)
# print("Beat positions (sec.):", beats)
# print("Beat estimation confidence:", beats_confidence)

# Melody Detection 

# Load audio file; it is recommended to apply equal-loudness filter for PredominantPitchMelodia
loader = EqloudLoader(filename='../data/flamenco.wav', sampleRate=44100)
audio = loader()
#print("Duration of the audio sample [sec]:")
#print(len(audio)/44100.0)

# frameSize = the frame size for computing pitch salience
# hop size = the hop size with which the pitch salience function was computed
pitch_extractor = PredominantPitchMelodia(frameSize=2048, hopSize=1024)
pitch_values, pitch_confidence = pitch_extractor(audio)

midi_extractor = PitchContourSegmentation(hopSize=1024)
onset, duration, midi_pitch = midi_extractor(pitch_values, audio)

# Pitch is estimated on frames. Compute frame time positions
pitch_times = numpy.linspace(0.0,len(audio)/44100.0,len(pitch_values) )

#Storing in Pool
pool.add('MIDIduration', duration)
pool.add('MIDIpitch', midi_pitch)
pool.add('pitch', pitch_values)
pool.add('beats', beats)
 
output = YamlOutput(format = 'json') # use "format = 'json'" for JSON output
output = YamlOutput(filename = 'output.json')
output(pool)