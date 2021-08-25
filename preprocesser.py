import pickle

import pretty_midi
import os
import music21
from music21 import note, chord, duration

import debug


def split_tracks_piano(path='piano'):
    output_path = 'split' + '/' + path
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')

    for midi_file_name in os.listdir('piano'):
        midi_file_name_without_ext = midi_file_name.split('.')[0]
        midi_file_name_with_path = path + '/' + midi_file_name
        midi_data = pretty_midi.PrettyMIDI(midi_file_name_with_path)

        for index in range(len(midi_data.instruments)):
            instrument = midi_data.instruments[index]
            output_midi_data = pretty_midi.PrettyMIDI()
            piano = pretty_midi.Instrument(program=piano_program)
            piano.notes = instrument.notes
            output_midi_data.instruments.append(piano)
            output_midi_data.write(output_path + '/' + midi_file_name_without_ext + '_track' + str(index) + '.mid')


def get_number_16th_note(length):
    if isinstance(length, duration.Duration):
        q_length = length.quarterLength
        return q_length // 0.25


def get_score(midi_notes):
    new_list = []
    for element in midi_notes:
        if isinstance(element, note.Rest) or isinstance(element, note.Note) or isinstance(element, chord.Chord):
            new_list.append(element)
    return new_list


def trim_rests(midi_notes):
    new_list = []
    content_begin = False
    for element in midi_notes:
        if content_begin:
            new_list.append(element)
        else:
            if not isinstance(element, note.Rest):
                content_begin = True
                new_list.append(element)

    return new_list


def quantize_sequence(midi_notes):
    list_to_save = []

    for element in midi_notes:
        duration_16th_note = duration.Duration()
        duration_16th_note.quarterLength = 0.25

        if isinstance(element, note.Note):
            number_of_16th_note = int(get_number_16th_note(element.duration)) + 1
            for i in range(number_of_16th_note):
                new_note = note.Note(pitchName=element.pitch, duration=duration_16th_note)
                print(str(new_note.pitch), 'duration:', str(new_note.duration.quarterLength))
                list_to_save.append(new_note)

        elif isinstance(element, note.Rest):
            # ensure there are at most 4 16th notes of rests, to avoid too many rests
            number_of_16th_note = int(get_number_16th_note(element.duration))
            if number_of_16th_note > 4:
                number_of_16th_note %= 4
            number_of_16th_note += 1
            for i in range(number_of_16th_note):
                new_rest = note.Rest(duration=duration_16th_note)
                print(new_rest.name, 'duration:', str(new_rest.duration.quarterLength))
                list_to_save.append(new_rest)

        elif isinstance(element, chord.Chord):
            number_of_16th_note = int(get_number_16th_note(element.duration)) + 1
            for i in range(number_of_16th_note):
                new_chord = chord.Chord(element.notes, duration=duration_16th_note)
                print('.'.join(str(n) for n in new_chord.normalOrder), 'duration:',
                      str(new_chord.duration.quarterLength))
                list_to_save.append(new_chord)

    return list_to_save


def get_pitches(midi_notes):
    new_list = []
    for element in midi_notes:
        if isinstance(element, note.Note):
            new_list.append(str(element.pitch))
        elif isinstance(element, note.Rest):
            new_list.append(element.name)
        elif isinstance(element, chord.Chord):
            new_list.append('.'.join(str(n) for n in element.normalOrder))


# def preprocess_piano(path='split/piano'):


def test():
    path = 'split/piano/rac_op23_2_track0.mid'
    midi_stream = music21.converter.parse(path)
    midi_notes = music21.instrument.partitionByInstrument(midi_stream).parts[0].recurse()
    tmp = get_score(midi_notes)
    re = trim_rests(tmp)
    # debug.music21_print_notes_sequence(re)
    quantized_notes = quantize_sequence(re)
    pickle.dump(get_pitches(quantized_notes), open('feed/tmp.p', 'wb'))
    debug.music21_print_notes_sequence(quantized_notes)
