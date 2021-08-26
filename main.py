import pickle

import music21
from music21 import duration, note

import data_preprocess
import debug
import sample_preprocess

# debug.test()
# debug.print_notes_sequence('dataset_piano/piano/lizet_et6_track2.mid')

# preprocesser.test()
# preprocesser.test_arcade()

# preprocesser.preprocess_piano()
# sample_preprocess.preprocess_arcade()
# data_preprocess.piano_midi_to_npy()
data_preprocess.arcade_midi_to_npy()
