import glob
import os

import pretty_midi
from music21 import note, chord


def file_number(path, extension='*'):
    return len(glob.glob(path + '/' + '*.' + extension))


def file_keep_extension(path, extension=None):
    if extension is None:
        extension = []

    for item in os.listdir(path):
        to_remove = True
        for e in extension:
            if item.endswith(e):
                to_remove = False
                break

        if to_remove:
            print('Removing:', item)
            os.remove(os.path.join(path, item))


def remove_single_track_samples(path, keyword):
    for item in os.listdir(path):
        if keyword in item:
            print('Removing:', item)
            os.remove(os.path.join(path, item))


def print_notes_sequence(file_name_with_path):
    midi_data = pretty_midi.PrettyMIDI(file_name_with_path)
    print('Number of notes:', len(midi_data.instruments[0].notes))
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            duration = note.end - note.start
            print(note.pitch, 'Duration = ', duration)


def music21_print_notes_sequence(midi_notes):
    for element in midi_notes:
        if isinstance(element, note.Note):
            print(str(element.pitch), '#' + str(int(element.pitch.ps)), 'duration:', str(element.duration.quarterLength))
        elif isinstance(element, note.Rest):
            print(element.name, 'duration:', str(element.duration.quarterLength))
        elif isinstance(element, chord.Chord):
            print('.'.join(str(int(n.ps)) for n in element.pitches), 'duration:', str(element.duration.quarterLength))


def test():
    print(file_number('piano'))
    remove_single_track_samples('piano', 'format0')
    # file_keep_extension(path='piano', extension=['mid', 'midi'])
    print(file_number('piano'))
