import pretty_midi
import os


def split_tracks_piano(path='piano'):
    output_path = 'split' + '/' + path
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')

    for midi_file_name in os.listdir(path):
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


def split_tracks_arcade(path='arcade'):
    output_path = 'split' + '/' + path
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')

    for midi_file_name in os.listdir(path):
        midi_file_name_without_ext = midi_file_name.split('.')[0]
        midi_file_name_with_path = path + '/' + midi_file_name
        try:
            midi_data = pretty_midi.PrettyMIDI(midi_file_name_with_path)

            for index in range(len(midi_data.instruments)):
                instrument = midi_data.instruments[index]
                if not instrument.is_drum:
                    output_midi_data = pretty_midi.PrettyMIDI()
                    piano = pretty_midi.Instrument(program=piano_program)
                    piano.notes = instrument.notes
                    output_midi_data.instruments.append(piano)
                    output_midi_data.write(
                        output_path + '/' + midi_file_name_without_ext + '_track' + str(index) + '.mid')
        except:
            print(midi_file_name, 'cannot be parsed')


def run():
    split_tracks_piano()
    split_tracks_arcade()
