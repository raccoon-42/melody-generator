import random

DURATIONS = [0.25, 0.5, 1, 2]  # Sixteenth, eighth, quarter, half notes
REST = -1  # Placeholder for silence/rest

NUM_BARS = 5
BEATS_PER_BAR = 4
# Define scale, chords, consonance values, and durations
# SCALE = [0, 2, 4, 5, 7, 9, 11]  # major scale
# SCALE = [0, 1, 3, 5, 7, 8, 10] # minor scale
SCALE = [0, 2, 3, 5, 7, 8, 11] # harmonic minor scale

def generate_random_melody(target_duration=(NUM_BARS-1)*BEATS_PER_BAR):
	melody = []
	total_duration = 0

	while total_duration < target_duration:
		current_bar = []
		current_bar_duration = 0

		while current_bar_duration < BEATS_PER_BAR:  # Limit to 4 beats per bar
			note = random.choice(SCALE + [REST])  # Add REST as an option
			duration = random.choice(DURATIONS)

			if current_bar_duration + duration > BEATS_PER_BAR:
				# Reset the current bar if adding this note exceeds 4 beats
				current_bar = []
				current_bar_duration = 0
			else:
				current_bar.append((note, duration))
				current_bar_duration += duration

		melody.extend(current_bar)
		total_duration += BEATS_PER_BAR
	return melody