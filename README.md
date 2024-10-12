# ConsolMP - Console MP3 Player

## Overview

ConsolMP is a console-based MP3 player developed in Python. It provides an intuitive interface for playing, pausing, and managing your music playlists. With features like volume control, mode switching, and rich console output, it enhances your music listening experience in a lightweight application.

## Features

- **Playlist Management**: Load and display playlists from a specified folder.
- **Playback Controls**: Play, pause, skip, and rewind songs easily.
- **Volume Adjustment**: Set and adjust volume levels dynamically.
- **Modes**: Switch between different playback modes (e.g., Random, Sequential).
- **Rich Console Output**: Interactive console interface with clear instructions and feedback.
- **Song Info Display**: Show current song details, including duration and playback position.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/glitchidea/ConsolMP.git
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.x installed. You can install the required libraries using pip:
   ```bash
   pip install pygame rich mutagen
   ```

## Usage

Run the player from the command line:

```bash
python main.py
```

### Commands

- **0**: Toggle between Random and Sequential modes.
- **1**: Toggle between different playback modes.
- **5**: Play/Pause the current song.
- **4**: Go to the previous song in the playlist.
- **6**: Skip to the next song.
- **7**: Rewind the song by 10 seconds.
- **9**: Fast forward the song by 10 seconds.
- **3**: Show the current playlist.
- **8**: Set volume level (0-10).
- **2**: Set the folder path for music files.
- **h**: Display help information.
- **q**: Exit the player.

## Security Considerations

- Ensure the music files are sourced legally.
- Keep your application updated to mitigate vulnerabilities.
