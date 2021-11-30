# this file contains the main class for the music engine
from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers import Composition
import mingus.extra.lilypond as lilypond
from mingus.midi import midi_file_out
import mingus.containers.note_container as nc
from mingus.midi import fluidsynth as fluid
from mingus.containers.instrument import MidiInstrument
import mingus.core.keys as keys
import numpy as np
import xarray as xr

class ocean_music_engine():

    # constants: # todo make this scales or harmonics at some point.
    _ALL_NOTES = {0:"C", 1:"C#", 2:"Db", 3:"D", 4:"D#", 5:"Eb", 6:"E", 7:"F", 8:"F#", 9:"Gb", 10:"G", 11:"G#", 12:"Ab", 13:"A", 14:"A#", 15:"Bb", 16:"B"}
    _LEN_ALL_NOTES = len(_ALL_NOTES)
    print(_LEN_ALL_NOTES)
    def _map_all_notes_to_0_1(self):
        # map all notes to the 0-1 interval
        temp_dict = {}
        for i in range(ocean_music_engine._LEN_ALL_NOTES):
            # will store a dictionary with ranges,
            # will use midpoints so there are exactly 17 intervals i.e. 0-0.5, 0.5-1.5, 1.5-2.5,
            # but the upper bound should fit between 0 and 16
            # will need i - 0.5 and i +
            # do correction on upper bound for interval:
            upper_bound_total = ocean_music_engine._LEN_ALL_NOTES - 1
            imhalf = i-0.5
            iphalf = i+0.5
            if imhalf <0: # cannot go below 0
                imhalf = 0
            if iphalf > upper_bound_total: # cannot go above notes limit
                iphalf = upper_bound_total

            lower_bound = (imhalf)/upper_bound_total
            upper_bound = (iphalf)/upper_bound_total
            # append onto dictionary:
            temp_dict[i] = [lower_bound,upper_bound]

        return temp_dict

    def __init__(self,data):
        self.data = data
        self.instrument = 15 # instrument to play
        self.music = None
        self.music_bpm = 150
        self.music_output_filename = "my_music_sheets.png"
        self.music_output_midi_filename = "my_music_midi.mid"

    # method for harmonizing the data before music generation # todo, this can be changed with other harmonizing engines
    def harmonize_data(self):
        # harmonize data by putting all values between 0 and 1
        data_max = np.nanmax(self.data)
        data_min = np.nanmin(self.data)
        temp_data = (self.data - data_min)/(data_max - data_min)
        # flatten
        temp_data = temp_data.values.flatten()
        # remove nan
        self.data = temp_data[np.logical_not(np.isnan(temp_data))]
        # print(self.data)
        pass

    # todo method for generating the music:
    def generate_music(self):
        print(self._map_all_notes_to_0_1())
        #
        # create bars on the time signature:
        for number in self.data:
            pass
        # add to tracks:

        # create composition from tracks:



        b = Bar()
        b + "C"
        b + "G"
        b + "E"
        b + "F#"
        print(b)
        self.music = b
        pass

    # todo method for playing music in midi file:
    def play_music_midi_file(self):
        if self.music is None:
            raise ValueError("Music not harmonized (generate_music()) and generated (generate_music())")
        # set instrument:
        i = MidiInstrument()
        i.instrument_nr = self.instrument # todo is this line needed??
        # load music font:
        fluid.init("soundfont.SF2")
        # todo write out midi file:
        midi_file_out.write_NoteContainer(self.music_output_midi_filename, nc.NoteContainer(["C", "D"]), self.music_bpm)
        # play the music:
        fluid.set_instrument(9, self.instrument)
        print("Playing music now...")
        fluid.play_Bar(self.music, 9, self.music_bpm)
        pass

    # todo generate the music sheet notation:
    def generate_musicsheets(self):
        # todo create the composition:
        barr = lilypond.from_Bar(self.music)
        # write to sheet music:
        lilypond.to_png(barr, self.music_output_filename)
        pass

    ## set and get methods:
    # set instrument:
    def set_instrument(self,instrument_type):
        self.instrument = instrument_type

    # set BPM:
    def set_music_bpm(self,music_bpm):
        self.music_bpm = music_bpm


if __name__ == '__main__':
    # data = np.array([[1,2,3],[3,4,5],[4,5,6]])
    data = xr.open_dataset("../data/20190101000000-GLOBCURRENT-L4-CUReul_15m-ALT_SUM_NRT-v03.0-fv01.0.nc")["u"]
    # print(data["u"].shape)
    music = ocean_music_engine(data)
    music.harmonize_data()
    music.generate_music()
    music.play_music_midi_file()
    music.generate_musicsheets()