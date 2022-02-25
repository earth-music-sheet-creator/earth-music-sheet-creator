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
import bisect

# plotting:
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



class ocean_music_engine():

    # constants: # todo make this scales or harmonics at some point.
    _ALL_NOTES = {0:"C", 1:"C#", 2:"Db", 3:"D", 4:"D#", 5:"Eb", 6:"E", 7:"F", 8:"F#", 9:"Gb", 10:"G", 11:"G#", 12:"Ab", 13:"A", 14:"A#", 15:"Bb", 16:"B"}
    _LEN_ALL_NOTES = len(_ALL_NOTES)
    # print(_LEN_ALL_NOTES)


    # https://stackoverflow.com/questions/53138434/use-range-as-a-key-value-in-a-dictionary-most-efficient-way
    # used for getting the note efficiently
    def _note_value_at_data_value(self,data_value,limits,notes):
        index = bisect.bisect_left(limits, data_value)
        return notes[index]

    def _map_all_notes_to_0_1(self):
        # map all notes to the 0-1 interval
        temp_dict = {}
        temp_list = []
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
            temp_list.append(upper_bound)

        return temp_dict,temp_list

    def __init__(self,data):
        self.data = data
        self.instrument = 1 # instrument to play
        self.music = None
        self.music_bpm = 150
        self.music_timesignature = (4,4)
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
        # self.data = temp_data[np.logical_not(np.isnan(temp_data))]
        self.data = temp_data[np.logical_not(np.isnan(temp_data))]#[0:1000] # because there is too many values, testing for now
        # print(self.data)
        print(len(self.data))
        pass

    def plot_data(self):
        print(self.data.shape)
        plt.figure()
        # x axis:
        plt.plot(np.arange(len(self.data)), self.data, "r-", label="x-axis")
        # y axis:
        # plt.legend()
        # plt.xlim([-self.axis_range, self.axis_range])
        # plt.ylim([0, 1000])
        plt.savefig("flattened_data_plot.png", bbox_inches="tight")

    # todo method for generating the music:
    def generate_music(self):
        # fourier transform method:
        fft = np.fft.rfft(self.data)
        fftfreq = np.fft.rfftfreq(len(self.data))

        # plot the frequencies:
        plt.figure()
        # x axis:
        plt.plot(fftfreq, fft, "r*", label="x-axis")
        # y axis:
        # plt.legend()
        # plt.xlim([-self.axis_range, self.axis_range])
        plt.ylim([0, 200])
        plt.savefig("fft_frequencies.png", bbox_inches="tight")


        # # get notes limits
        # temp_dict,notes_limits = self._map_all_notes_to_0_1()
        #
        # # Test bar time signature:
        # try:
        #     Bar(meter=self.music_timesignature)
        # except Exception as e:
        #     raise ValueError("The music time signature is invalid, please use another time signature.")
        #
        # # create the track:
        # main_track  = Track(MidiInstrument(name="Violin"))
        #
        # # create bars on the time signature:
        # # reshape data
        # m, n = 17000, int(len(self.data)/17000)+1
        # self.data = np.pad(self.data.astype(float), (0, m * n - self.data.size),
        #        mode='constant', constant_values=1.0).reshape(m, n)
        # b = Bar(meter=self.music_timesignature)
        # # for index,number in enumerate(self.data):
        # for index,number in enumerate(range(n)):
        #     if index%self.music_timesignature[1] == 0:
        #         b = Bar(meter=self.music_timesignature) # make it empty again
        #     # find note to add
        #     new_data_point = np.sum(self.data[:,number])/m # average the values to get something in-between 0 and 1
        #     print(new_data_point)
        #     b + self._note_value_at_data_value(new_data_point,notes_limits,ocean_music_engine._ALL_NOTES)
        #
        #     # add to tracks:
        #     main_track.add_bar(b)
        #     pass
        #
        # # create composition from tracks:
        # composition = Composition()
        # composition.set_author('Kirodh Boodhraj', 'kboodhraj@gmail.com')
        # composition.set_title('First Mingus Composition')
        # composition.add_track(main_track)
        #
        # self.music = composition
        # pass

    # todo method for playing music in midi file:
    def play_music_midi_file(self):
        if self.music is None:
            raise ValueError("Music not harmonized (generate_music()) and generated (generate_music())")
        # set instrument:
        i = MidiInstrument(name="violin")
        i.instrument_nr = self.instrument # todo is this line needed??
        # load music font:
        fluid.init("soundfont.SF2")
        # todo write out midi file:
        midi_file_out.write_Composition(self.music_output_midi_filename, self.music, self.music_bpm)
        # play the music:
        fluid.set_instrument(9, self.instrument,bank=128)
        print("Playing music now...")
        # fluid.play_Bar(self.music, 9, self.music_bpm)
        fluid.play_Composition(self.music, 9, self.music_bpm)
        pass

    # todo generate the music sheet notation:
    def generate_musicsheets(self):
        # todo create the composition:
        # barr = lilypond.from_Bar(self.music)
        barr = lilypond.from_Composition(self.music)
        # write to sheet music:
        # lilypond.to_png(barr, self.music_output_filename)
        lilypond.to_pdf(barr, self.music_output_filename)
        pass

    ## set and get methods:
    # set instrument:
    def set_instrument(self,instrument_type):
        self.instrument = instrument_type

    # set BPM:
    def set_music_bpm(self,music_bpm):
        self.music_bpm = music_bpm

    # set timesignature:
    def set_music_timesignature(self,music_timesignature):
        self.music_timesignature = music_timesignature


if __name__ == '__main__':
    print("open data:")
    # data = np.array([[1,2,3],[3,4,5],[4,5,6]])
    data = xr.open_dataset("../data/20190101000000-GLOBCURRENT-L4-CUReul_15m-ALT_SUM_NRT-v03.0-fv01.0.nc")["u"]
    # print(data["u"].shape)
    print("create music object:")
    music = ocean_music_engine(data)
    print("harmonize data:")
    music.harmonize_data()
    # music.set_music_timesignature((4,3))
    print("plot data:")
    music.plot_data()
    print("generate music:")
    music.generate_music()
    print("play music:")
    # music.play_music_midi_file()
    print("make sheet music:")
    # music.generate_musicsheets()