import mido
import json
import argparse

MIDI_INSTRUMENTS = {
    0: "Acoustic Grand Piano",
    1: "Bright Acoustic Piano",
    2: "Electric Grand Piano",
    3: "Honky-tonk Piano",
    4: "Electric Piano 1",
    5: "Electric Piano 2",
    6: "Harpsichord",
    7: "Clavinet",
    8: "Celesta",
    9: "Glockenspiel",
    10: "Music Box",
    11: "Vibraphone",
    12: "Marimba",
    13: "Xylophone",
    14: "Tubular Bells",
    15: "Dulcimer",
    16: "Drawbar Organ",
    17: "Percussive Organ",
    18: "Rock Organ",
    19: "Church Organ",
    20: "Reed Organ",
    21: "Accordion",
    22: "Harmonica",
    23: "Tango Accordion",
    24: "Acoustic Guitar (nylon)",
    25: "Acoustic Guitar (steel)",
    26: "Electric Guitar (jazz)",
    27: "Electric Guitar (clean)",
    28: "Electric Guitar (muted)",
    29: "Overdriven Guitar",
    30: "Distortion Guitar",
    31: "Guitar harmonics",
    32: "Acoustic Bass",
    33: "Electric Bass (finger)",
    34: "Electric Bass (pick)",
    35: "Fretless Bass",
    36: "Slap Bass 1",
    37: "Slap Bass 2",
    38: "Synth Bass 1",
    39: "Synth Bass 2",
    40: "Violin",
    41: "Viola",
    42: "Cello",
    43: "Contrabass",
    44: "Tremolo Strings",
    45: "Pizzicato Strings",
    46: "Orchestral Harp",
    47: "Timpani",
    48: "String Ensemble 1",
    49: "String Ensemble 2",
    50: "Synth Strings 1",
    51: "Synth Strings 2",
    52: "Choir Aahs",
    53: "Voice Oohs",
    54: "Synth Voice",
    55: "Orchestra Hit",
    56: "Trumpet",
    57: "Trombone",
    58: "Tuba",
    59: "Muted Trumpet",
    60: "French Horn",
    61: "Brass Section",
    62: "Synth Brass 1",
    63: "Synth Brass 2",
    64: "Soprano Sax",
    65: "Alto Sax",
    66: "Tenor Sax",
    67: "Baritone Sax",
    68: "Oboe",
    69: "English Horn",
    70: "Bassoon",
    71: "Clarinet",
    72: "Piccolo",
    73: "Flute",
    74: "Recorder",
    75: "Pan Flute",
    76: "Blown Bottle",
    77: "Shakuhachi",
    78: "Whistle",
    79: "Ocarina",
    80: "Square Lead",
    81: "Sawtooth Lead",
    82: "Calliope Lead",
    83: "Chiff Lead",
    84: "Charang Lead",
    85: "Voice Lead",
    86: "Fifths Lead",
    87: "Bass & Lead",
    88: "New Age Pad",
    89: "Warm Pad",
    90: "Polysynth Pad",
    91: "Choir Pad",
    92: "Bowed Pad",
    93: "Metallic Pad",
    94: "Halo Pad",
    95: "Sweep Pad",
    96: "Rain Pad",
    97: "Soundtrack Pad",
    98: "Crystal Pad",
    99: "Atmosphere Pad",
    100: "Brightness Pad",
    101: "Goblin Pad",
    102: "Echoes Pad",
    103: "Sci-fi Pad",
    104: "Sitar",
    105: "Banjo",
    106: "Shamisen",
    107: "Koto",
    108: "Kalimba",
    109: "Bag pipe",
    110: "Fiddle",
    111: "Shanai",
    112: "Tinkle Bell",
    113: "Agogo",
    114: "Steel Drums",
    115: "Woodblock",
    116: "Taiko Drum",
    117: "Melodic Tom",
    118: "Synth Drum",
    119: "Reverse Cymbal",
    120: "Guitar Fret Noise",
    121: "Breath Noise",
    122: "Seashore",
    123: "Bird Tweet",
    124: "Telephone Ring",
    125: "Helicopter",
    126: "Applause",
    127: "Gunshot"
}

def convertNoteToName(note):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return notes[note % 12] + str(note // 12 - 1)

class MusicNote:
    def __init__(self, note, duration, position):
        self.note = note
        self.duration = duration
        self.position = position

    def __str__(self):
        return f"{self.note} {self.duration:.2f}s {self.position:.2f}s"
    
    def to_dict(self):
        return {
            'note': self.note,
            'duration': self.duration,
            'position': self.position,
            "note_name": convertNoteToName(self.note)
        }
    
class MidiTrack:
    def __init__(self, track_name, instrument):
        self.track_name = track_name
        self.instrument = instrument
        self.notes = []
        self.tempo = 120  # Default tempo
        
    def addNote(self, note, duration, position):
        self.notes.append(MusicNote(note, duration, position))
        
    def __str__(self):
        return f"{self.track_name} ({self.instrument}, {self.tempo} BPM): {self.notes}"
    
    def to_dict(self):
        return {
            'track_name': self.track_name,
            'instrument': self.instrument,
            'tempo': self.tempo,
            'notes': [note.to_dict() for note in self.notes]
        }
    
class MidiConverter:
    def __init__(self, midi_file):
        self.midi_file = midi_file
        self.tracks = {}
        self.parseMidi()

    def parseMidi(self):
        midi = mido.MidiFile(self.midi_file)
        ticks_per_beat = midi.ticks_per_beat
        for i, track in enumerate(midi.tracks):
            track_name = f"Track {i}"
            instrument = "Unknown"
            midi_track = MidiTrack(track_name, instrument)
            position = 0
            tempo = 500000  # Default tempo in microseconds per beat (120 BPM)
            note_on_times = {}
            for msg in track:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    midi_track.tempo = mido.tempo2bpm(tempo)
                elif msg.type == 'note_on' and msg.velocity > 0:
                    note_on_times[msg.note] = position
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in note_on_times:
                        start_time = note_on_times.pop(msg.note)
                        time_per_tick = tempo / 1_000_000 / ticks_per_beat
                        duration_in_seconds = (position - start_time) * time_per_tick
                        position_in_seconds = start_time * time_per_tick
                        midi_track.addNote(msg.note, duration_in_seconds, position_in_seconds)
                elif msg.type == 'program_change':
                    instrument = MIDI_INSTRUMENTS.get(msg.program, "Unknown")
                    midi_track.instrument = instrument
                position += msg.time
            self.tracks[track_name] = midi_track

    def printTrackInfo(self):
        for track in self.tracks.values():
            print(f"Track: {track.track_name} Instrument: {track.instrument} BPM: {track.tempo} Note Count: {len(track.notes)}")
    
    def to_dict(self):
        return {
            'midi_file': self.midi_file,
            'tracks': {name: track.to_dict() for name, track in self.tracks.items()}
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert MIDI files to JSON.")
    parser.add_argument("-i", "--input", required=True, help="Input MIDI file")
    parser.add_argument("-o", "--output", default="output.json", help="Output JSON file (default: output.json)")
    args = parser.parse_args()

    converter = MidiConverter(args.input)
    converter.printTrackInfo()

    # Convert to JSON
    json_data = json.dumps(converter.to_dict(), indent=4)
    with open(args.output, "w") as f:
        f.write(json_data)