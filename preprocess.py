import pretty_midi
import os
import music21


def process_piano(path='piano'):
    output_path = 'test_output' + '/' + path
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


def test():
    # path = 'arcade/Boom_Boom_Dollar.mid'
    path = 'piano/alb_esp1.mid'
    midi_data = pretty_midi.PrettyMIDI(path)
    print(midi_data.key_signature_changes[0])
    # # total_velocity = sum(sum(midi_data.get_chroma()))
    # # print[sum(semitone) / total_velocity for semitone in midi_data.get_chroma()]

    # output_path = 'test_output/piano'
    # cello_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    #
    # for index in range(len(midi_data.instruments)):
    #     instrument = midi_data.instruments[index]
    #     output_midi_data = pretty_midi.PrettyMIDI()
    #
    #     cello = pretty_midi.Instrument(program=cello_program)
    #     cello.notes = instrument.notes
    #     output_midi_data.instruments.append(cello)
    #     output_midi_data.write(output_path + '/' + 'lizet_et6' + '_track' + str(index) + '.mid')
