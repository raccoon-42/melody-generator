import os
from datetime import datetime
import mido
from mido import MidiFile, MidiTrack, Message
import pygame

import music

NOTE_BASE = 59
BPM = 80

def create_midi_file(melody, chords, beats_per_bar=music.BEATS_PER_BAR, REST=music.REST, NOTE_BASE=NOTE_BASE):
	# Create 'melodies' folder if it doesn't exist
	output_folder = "melodies"
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	# Generate filename with timestamp
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = os.path.join(output_folder, f"melodie_{timestamp}.mid")

	mid = MidiFile()
	melody_track = MidiTrack()
	chord_track = MidiTrack()
	mid.tracks.append(melody_track)
	mid.tracks.append(chord_track)

	# Set tempo
	melody_track.append(mido.MetaMessage('set_tempo', tempo=60000000//BPM))
	chord_track.append(mido.MetaMessage('set_tempo', tempo=60000000//BPM))

	# Add melody to the melody track
	current_time = 0
	for note, duration in melody:
		time = int(duration * 480)  # Convert duration to MIDI ticks
		if note == REST:
			# Silence: Only delay without note_on/note_off
			melody_track.append(Message('note_off', note=0, velocity=0, time=time))
		else:
			midi_note = NOTE_BASE + note
			melody_track.append(Message('note_on', note=midi_note, velocity=64, time=0))
			melody_track.append(Message('note_off', note=midi_note, velocity=64, time=time))
		current_time += time

	# Add chords to the chord track
	current_time = 0
	for bar_index, chord in enumerate(chords):
		chord_notes = [NOTE_BASE + int(note) for note in chord]

		# Play each chord for the duration of the bar
		for note in chord_notes:
			chord_track.append(Message('note_on', note=note, velocity=50, time=0))
		chord_track.append(Message('note_off', note=chord_notes[0], velocity=50, time=beats_per_bar * 480))
		for note in chord_notes[1:]:
			chord_track.append(Message('note_off', note=note, velocity=50, time=0))
		current_time += beats_per_bar * 480

	# Save the MIDI file in the 'melodies' folder
	mid.save(filename)
	print(f"MIDI file saved as {filename}")
	return filename


def play_midi_file(filename):
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play()
	print("Playing melody...")
	while pygame.mixer.music.get_busy():
		pygame.time.wait(100)
	pygame.quit()