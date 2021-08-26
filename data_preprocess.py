import os
import pickle

import pypianoroll
import numpy as np
import matplotlib.pyplot as plt
import music21
from music21 import note, chord, duration

import debug
import sample_preprocess


def get_index_in_matrix_by_pitch(pitch):
    if isinstance(pitch, music21.pitch.Pitch):
        p = int(pitch.ps)
        if p > 108 or p < 25:
            return -1
        else:
            return p - 25


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


def get_number_16th_note(length):
    if isinstance(length, duration.Duration):
        q_length = length.quarterLength
        return q_length // 0.25


def quantize_sequence(midi_notes):
    list_to_save = []

    for element in midi_notes:
        duration_16th_note = duration.Duration()
        duration_16th_note.quarterLength = 0.25

        if isinstance(element, note.Note):
            number_of_16th_note = int(get_number_16th_note(element.duration)) + 1
            for i in range(number_of_16th_note):
                new_note = note.Note(pitchName=element.pitch, duration=duration_16th_note)
                # print(str(new_note.pitch), 'duration:', str(new_note.duration.quarterLength))
                list_to_save.append(new_note)

        elif isinstance(element, note.Rest):
            # ensure there are at most 4 16th notes of rests, to avoid too many rests
            number_of_16th_note = int(get_number_16th_note(element.duration))
            if number_of_16th_note > 4:
                number_of_16th_note %= 4
            number_of_16th_note += 1
            for i in range(number_of_16th_note):
                new_rest = note.Rest(duration=duration_16th_note)
                # print(new_rest.name, 'duration:', str(new_rest.duration.quarterLength))
                list_to_save.append(new_rest)

        elif isinstance(element, chord.Chord):
            number_of_16th_note = int(get_number_16th_note(element.duration)) + 1
            for i in range(number_of_16th_note):
                new_chord = chord.Chord(element.notes, duration=duration_16th_note)
                # print('.'.join(str(n) for n in new_chord.normalOrder), 'duration:',
                #       str(new_chord.duration.quarterLength))
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
    return new_list


def piano_midi_to_npy(path='split/piano'):
    npy_count = 0
    midi_file_list = os.listdir(path)
    for midi_file in midi_file_list:
        tmp_path = path + '/' + midi_file
        midi_stream = music21.converter.parse(tmp_path)
        midi_notes = music21.instrument.partitionByInstrument(midi_stream).parts[0].recurse()
        re = trim_rests(get_score(midi_notes))
        quantized_notes = quantize_sequence(re)
        pitch_list = quantized_notes
        batch_64_count = 0
        while (batch_64_count * 64 + 64) < len(pitch_list):
            n = np.zeros(shape=(64, 84, 1), dtype=np.bool)
            for i in range(64):
                element = pitch_list[batch_64_count * 64 + i]
                if isinstance(element, note.Note):
                    n[i, get_index_in_matrix_by_pitch(element.pitch), 0] = True
                elif isinstance(element, note.Rest):
                    continue
                elif isinstance(element, chord.Chord):
                    for p in element.pitches:
                        n[i, get_index_in_matrix_by_pitch(p), 0] = True
            filename = 'datasets/piano/piano' + str(npy_count) + '.npy'
            np.save(file=filename, arr=n)
            batch_64_count += 1
            npy_count += 1
        print('Parse finished:', midi_file, 'Current npy index:', str(npy_count))


def arcade_midi_to_npy(path='split/arcade'):
    npy_count = 0
    midi_file_list = os.listdir(path)
    for midi_file in midi_file_list:
        try:
            tmp_path = path + '/' + midi_file
            midi_stream = music21.converter.parse(tmp_path)
            midi_notes = music21.instrument.partitionByInstrument(midi_stream).parts[0].recurse()
            re = trim_rests(get_score(midi_notes))
            quantized_notes = quantize_sequence(re)
            pitch_list = quantized_notes
            batch_64_count = 0
            while (batch_64_count * 64 + 64) < len(pitch_list):
                n = np.zeros(shape=(64, 84, 1), dtype=np.bool)
                for i in range(64):
                    element = pitch_list[batch_64_count * 64 + i]
                    if isinstance(element, note.Note):
                        n[i, get_index_in_matrix_by_pitch(element.pitch), 0] = True
                    elif isinstance(element, note.Rest):
                        continue
                    elif isinstance(element, chord.Chord):
                        for p in element.pitches:
                            n[i, get_index_in_matrix_by_pitch(p), 0] = True
                filename = 'datasets/arcade/arcade' + str(npy_count) + '.npy'
                np.save(file=filename, arr=n)
                batch_64_count += 1
                npy_count += 1
            print('Parse finished:', midi_file, 'Current npy index:', str(npy_count))
        except:
            print('Parsing FAILED:', midi_file)

# def preprocess_piano(path='split/piano'):
#     data_list = []
#     count = 0
#     for midi_file in os.listdir(path):
#         tmp_path = path + '/' + midi_file
#         midi_stream = music21.converter.parse(tmp_path)
#         midi_notes = music21.instrument.partitionByInstrument(midi_stream).parts[0].recurse()
#         re = trim_rests(get_score(midi_notes))
#         quantized_notes = quantize_sequence(re)
#         pitch_only_list = get_pitches(quantized_notes)
#         data_list += pitch_only_list
#         count += 1
#         print('Parsing finished:', midi_file)
#         if count % 25 == 0:
#             pickle.dump(data_list, open('feed/piano' + str(count // 25) + '.p', 'wb'))
#             data_list = []
#
#
# def preprocess_arcade(path='split/arcade'):
#     data_list = []
#     count = 0
#     for midi_file in os.listdir(path):
#         try:
#             tmp_path = path + '/' + midi_file
#             midi_stream = music21.converter.parse(tmp_path)
#             midi_notes = music21.instrument.partitionByInstrument(midi_stream).parts[0].recurse()
#             re = trim_rests(get_score(midi_notes))
#             quantized_notes = quantize_sequence(re)
#             pitch_only_list = get_pitches(quantized_notes)
#             data_list += pitch_only_list
#             count += 1
#             print('Parsing finished:', midi_file)
#             if count % 50 == 0:
#                 pickle.dump(data_list, open('feed/arcade' + str(count // 50) + '.p', 'wb'))
#                 data_list = []
#         except:
#             print('Parsing FAILED:', midi_file)
