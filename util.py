import music

def display_melody(best_fitness, best_melody):
	print("\nBest Melody and Fitness Scores:")
	print(f"Consonance Score: {best_fitness[0]}, Dissonance Resolution Score: {best_fitness[1]}, Rhythm Consistency Score: {best_fitness[2]}")
	for note, duration in best_melody:
		note_name = "REST" if note == music.REST else f"Note: {note}"
		print(f"{note_name}, Duration: {duration}")