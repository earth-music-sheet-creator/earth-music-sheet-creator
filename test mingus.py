# import mingus.containers.bar as bar
from mingus.containers import Bar
import mingus.core.keys as scales
import mingus.extra.lilypond as lilypond
from mingus.midi import midi_file_out
import mingus.containers.note_container as nc
from mingus.midi import fluidsynth as a
from mingus.containers.instrument import MidiInstrument

# print([notes.int_to_note(i) for i in range(12)])
# print(scales.get_notes("C#"))

b = Bar()
b + "C"
b + "G"
b + "E"
b + "F#"

barr = lilypond.from_Bar(b)
lilypond.to_png(barr, "my_first_bar")

i = MidiInstrument()
i.instrument_nr = 20

midi_file_out.write_NoteContainer("hi.mid",nc.NoteContainer(["C","D"]),120)
a.init("ocean_music/soundfont.SF2")
a.set_instrument(1,6)
a.play_Bar(b, 1, 150)

