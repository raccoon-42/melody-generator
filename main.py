import midi, ea, util

# this input can be generic, can be taken from user
# --------------------------------------------------
CHORD_PROGRESSIONS = [
	[0, 3, 7],   # i (B Minor)
	[3, 7, 11],  # III (D Major)
	[8, 0, 3],   # VI (G Major)
	[7, 11, 2],  # V (F# Major)
	[0, 3, 7],   # i (B Minor)
]

# --------------------------------------------------

# Run GA and get best melody and its fitness scores
best_fitness, best_melody = ea.genetic_algorithm(CHORD_PROGRESSIONS)
util.display_melody(best_fitness, best_melody)

# Save and play melody
filename = midi.create_midi_file(best_melody, CHORD_PROGRESSIONS)
midi.play_midi_file(filename)
