# Melody Generator

A Python-based melody generator that uses genetic algorithms to create musical melodies based on chord progressions.

## Description

This project generates musical melodies using a genetic algorithm approach. It takes chord progressions as input and evolves melodies that fit harmonically with the given chords. The generated melodies can be played directly or saved as MIDI files.

## Features

- Genetic algorithm-based melody generation
- Support for custom chord progressions
- MIDI file generation and playback
- Harmonic fitness evaluation
- Real-time melody playback

## Requirements

- Python 3.x
- Required Python packages (see `requirements.txt`):
  - mido==1.3.3
  - packaging==24.2
  - pygame==2.6.1

## Installation

1. Clone the repository:
```bash
git clone https://github.com/raccoon-42/melody-generator.git
cd melody-generator
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Modify the chord progressions in `main.py` according to your needs. By default, the program uses the chord progression from Polyphia's "GOAT" song in B minor.

2. Run the program:
```bash
python main.py
```

The program will:
- Generate a melody using the genetic algorithm
- Display the fitness score of the best melody
- Create a MIDI file of the generated melody
- Play the melody using your system's MIDI output

## Project Structure

- `main.py` - Main entry point and chord progression configuration
- `ea.py` - Genetic algorithm implementation
- `music.py` - Music theory and melody generation functions
- `midi.py` - MIDI file handling and playback
- `util.py` - Utility functions
- `melodies/` - Directory for generated MIDI files

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 