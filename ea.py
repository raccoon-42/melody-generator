import random
import music

# HYPERPARAMETERS
MR = 0.1
CR = 0.1
NP = 100
G = 10000

# Reward and Penalty Configuration
SILENCE_REWARD = 1

CHORD_ALIGNMENT_REWARD = 100
CHORD_UNALIGNMENT_PENALTY = -30

SCALE_CONSONANCE_WEIGHTS = [10, 7, 8, 5, 9, 4, 3]
SCALE_CONSONANCE_WEIGHT_MULTIPLIER = 5
SCALE_VIOLATION_PENALTY = -10

ON_BEAT_REWARD = 100
OFF_BEAT_PENALTY = -50

DISSONANCE_RESOLUTION_REWARD = 100
DISSONANCE_UNRESOLVED_PENALTY = -50

HARMONIC_RESOLUTION_REWARD = 100
HARMONIC_RESOLUTION_PENALTY = -100

BAR_DURATION_VIOLATION_PENALTY = -2000

def __init__(self, MR, CR, NP, G):
	self.MR = MR
	self.CR = CR
	self.NP = NP
	self.G = G

def crossover(parent1, parent2, crossover_rate):
	if random.random() < crossover_rate:  # Perform crossover with probability CR
		point = random.randint(1, len(parent1) - 1)
		return parent1[:point] + parent2[point:]
	else:  # Skip crossover, return one of the parents
		return random.choice([parent1, parent2])


def mutate(melody, scale, durations, mutation_rate, REST=music.REST):
	for i in range(len(melody)):
		if random.random() < mutation_rate:
			note = random.choice(scale + [REST])
			duration = random.choice(durations)
			melody[i] = (note, duration)
	return melody

def fitness_function_multiobjective(melody, chords, scale, beats_per_bar=music.BEATS_PER_BAR, REST=music.REST):
	"""
	Evaluate the fitness of a melody with multiobjective optimization for:
	1. Consonance
	2. Dissonance resolution
	3. Rhythm consistency (penalize notes that don't align with the beat)
	"""
	consonance_score = 0
	dissonance_resolution_score = 0
	rhythm_consistency_score = 0
	total_duration = sum(duration for _, duration in melody)

	if total_duration != beats_per_bar * len(chords):
		return BAR_DURATION_VIOLATION_PENALTY, BAR_DURATION_VIOLATION_PENALTY, BAR_DURATION_VIOLATION_PENALTY

	# Split melody into bars
	bars = []
	current_bar = []
	current_bar_duration = 0

	for note, duration in melody:
		current_bar.append((note, duration))
		current_bar_duration += duration

		if current_bar_duration == beats_per_bar:  # Complete the current bar
			bars.append(current_bar)
			current_bar = []
			current_bar_duration = 0

	# Evaluate each bar
	for bar_index, bar in enumerate(bars):
		if bar_index >= len(chords):
			break  # Ignore bars beyond the provided chords

		current_chord = chords[bar_index]
		bar_duration = sum(duration for _, duration in bar)

		if bar_duration != beats_per_bar:
			consonance_score += BAR_DURATION_VIOLATION_PENALTY

		last_note = None
		note_start = 0  # Track the start time of notes in the bar

		for note, duration in bar:
			if note == REST:
				consonance_score += SILENCE_REWARD * duration  # Reward for silences
				note_start += duration
				last_note = note
				continue

			# Check chord alignment
			if note in current_chord:
				consonance_score += CHORD_ALIGNMENT_REWARD * duration
			else:
				consonance_score += CHORD_UNALIGNMENT_PENALTY * duration

			# Check scale compliance
			if note not in scale:
				consonance_score += SCALE_VIOLATION_PENALTY * duration

			# Reward consonance
			if note in scale:
				degree = scale.index(note)
				consonance_score += SCALE_CONSONANCE_WEIGHTS[degree] * duration * SCALE_CONSONANCE_WEIGHT_MULTIPLIER

			# Penalize notes that don't start on beats
			if note_start % 1 != 0:  # Check if the note starts off-beat
				rhythm_consistency_score += OFF_BEAT_PENALTY
			else:
				rhythm_consistency_score += ON_BEAT_REWARD

			# Dissonance resolution
			if last_note is not None and last_note not in current_chord:
				if note in current_chord:  # Resolves into consonance
					dissonance_resolution_score += DISSONANCE_RESOLUTION_REWARD
				else:  # Unresolved dissonance
					dissonance_resolution_score += DISSONANCE_UNRESOLVED_PENALTY

			last_note = note
			note_start += duration

	# Ensure the last bar resolves harmonically
	last_bar = bars[-1] if bars else []
	last_bar_chord = chords[-1] if chords else []
	for note, _ in last_bar:
		if note in last_bar_chord:
			consonance_score += HARMONIC_RESOLUTION_REWARD
		elif note != REST:
			consonance_score += HARMONIC_RESOLUTION_PENALTY

	return consonance_score, dissonance_resolution_score, rhythm_consistency_score


def genetic_algorithm(CHORD_PROGRESSIONS, pop_size=NP, generations=G, MR=MR, CR=CR,
					  SCALE=music.SCALE, num_bars=music.NUM_BARS-1, beats_per_bar=music.BEATS_PER_BAR,
					  DURATIONS=music.DURATIONS):

	target_duration = num_bars * beats_per_bar
	population = [music.generate_random_melody(target_duration) for _ in range(pop_size)]
	best_fitness = (-float("inf"), -float("inf"), -float("inf"))
	best_melody = None

	for generation in range(generations):
		fitness_scores = [
			(fitness_function_multiobjective(m, CHORD_PROGRESSIONS[:num_bars], SCALE, beats_per_bar), m)
			for m in population
		]
		fitness_scores.sort(reverse=True, key=lambda x: (x[0][0], x[0][1], x[0][2]))

		# Print generation information
		current_best_fitness = fitness_scores[0][0]
		print(f"Generation {generation}: Best Fitness = {current_best_fitness}")

		# Update best fitness and melody
		if current_best_fitness > best_fitness:
			best_fitness = current_best_fitness
			best_melody = fitness_scores[0][1]

		# Select parents
		parents = [m for _, m in fitness_scores[:pop_size // 2]]
		next_gen = []
		for i in range(0, len(parents), 2):
			p1, p2 = parents[i], parents[(i + 1) % len(parents)]

			# Use crossover with fallback logic
			child1 = crossover(p1, p2, CR)
			child2 = crossover(p2, p1, CR)

			# Ensure diversity in children
			if child1 == child2:
				child2 = mutate(child2, SCALE, DURATIONS, MR)  # Force a mutation to diversify

			# Apply mutation to both children
			child1 = mutate(child1, SCALE, DURATIONS, MR)
			child2 = mutate(child2, SCALE, DURATIONS, MR)

			next_gen.extend([child1, child2])
		population = next_gen

	return best_fitness, best_melody