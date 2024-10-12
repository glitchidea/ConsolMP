import time
import os
import json
import pygame
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from mutagen.mp3 import MP3

# Initialize Pygame
pygame.mixer.init()

# Rich console
console = Console()

# Settings file
settings_file = "ConsolMp.json"

def clear_screen():
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def scii_art():
    art = """
                 /           /                                               
                /' .,,,,  ./                                                 
               /';'     ,/                                                   
              / /   ,,//,`'`                                                 
             ( ,, '_,  ,,,' ``                                               
             |    /@  ,,, ;" `                                               
            /    .   ,''/' `,``                                              
           /   .     ./, `,, ` ;                                             
        ,./  .   ,-,',` ,,/''\,'                                             
       |   /; ./,,'`,,'' |   |                                               
       |     /   ','    /    |                                               
        \___/'   '     |     |                                               
          `,,'  |      /     `\                                              
               /      |        ~\                                            
  Consol      '       (                                                      
     MP      :                                                               
            ; .         \--                                                  
          :   \         ;

    """
    # Get the screen size
    print(art)

def show_help():
    help_text = """
      -  MENU  -
0 - Mode   (currently: Random)
1 - Mode2  (Instant: Repeat)
5 - Stop/Start Song
4 - Go to Previous Song
6 - Go to Next Song
7 - Rewind 10 seconds
9 - Fast Forward 10 seconds
3 - Show Playlist
8 - Set Volume Level (0-10)
2 - Set File Path
h - Info About the Song
q - Exit
    """
    console.print(help_text)

class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_index = 0
        self.mode = 'Random'  # Initial mode
        self.mode2 = 'Repeat'  # Initial mode2
        self.is_playing = False
        self.volume = 0.5  # Volume level
        self.folder_path = ""  # Initial folder path is empty
        self.load_settings()  # Load settings
        self.load_playlist()  # Load playlist
        self.queue = []  # Song queue

    def load_settings(self):
        """Loads the file path from the settings file."""
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as file:
                settings = json.load(file)
                self.folder_path = settings.get("folder_path", "")
                console.print(f"[green]Settings loaded:[/] Folder path: {self.folder_path}")
        else:
            console.print("[yellow]Settings file not found. Set a new path.[/]")

    def save_settings(self):
        """Saves the settings to a file."""
        settings = {
            "folder_path": self.folder_path
        }
        with open(settings_file, 'w') as file:
            json.dump(settings, file)
            console.print("[green]Settings saved.[/]")

    def load_playlist(self):
        """Loads MP3 files from the specified folder."""
        if self.folder_path:
            self.playlist = [f for f in os.listdir(self.folder_path) if f.endswith('.mp3')]
            console.print(f"[green]Playlist loaded:[/] Found {len(self.playlist)} songs.")
        else:
            console.print("[red]Folder path not set![/]")

    def show_playlist(self):
        """Displays the playlist."""
        table = Table(title="Playlist")
        table.add_column("Index", justify="center")
        table.add_column("Song Name", justify="left")

        for index, song in enumerate(self.playlist):
            table.add_row(str(index + 1), song)

        console.print(table)

    def play_song(self):
        """Plays the song."""
        if self.playlist:
            song_path = os.path.join(self.folder_path, self.playlist[self.current_index])
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.volume)  # Set volume level
            pygame.mixer.music.play()
            self.is_playing = True
            self.show_current_song_info()  # Show info about the current song
        else:
            console.print("[red]Playlist is empty![/]")

    def toggle_play_pause(self):
        """Pauses or resumes the song."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            console.print("[yellow]Song paused.[/]")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            console.print("[green]Song is continuing.[/]")

    def next_song(self):
        """Goes to the next song."""
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()
        else:
            console.print("[red]Playlist is empty![/]")

    def previous_song(self):
        """Goes to the previous song."""
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()
        else:
            console.print("[red]Playlist is empty![/]")

    def seek_forward(self, seconds):
        """Fast forwards the song by the specified seconds."""
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # Get current time in seconds
            new_time = current_time + seconds
            pygame.mixer.music.set_pos(new_time)
            console.print(f"[green]Song fast forwarded by {seconds} seconds.[/]")

    def seek_backward(self, seconds):
        """Rewinds the song by the specified seconds."""
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # Get current time in seconds
            new_time = max(0, current_time - seconds)  # Limit time to not go below 0
            pygame.mixer.music.set_pos(new_time)
            console.print(f"[green]Song rewound by {seconds} seconds.[/]")  

    def seek_to_time(self, minutes):
        """Sets the song to the specified minute."""
        if self.is_playing:
            current_pos = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
            new_pos = minutes * 60  # Convert minutes to seconds
            
            # Set position by playing audio without using FFmpeg
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=new_pos)
            
            console.print(f"[green]Song set to {minutes} minutes.[/]")
        else:
            console.print("[red]Song is not playing![/]")

    def ffmpeg_seek(self, file_path, seconds, backward=False):
        """Seeks the song forward or backward using FFmpeg."""
        current_position = pygame.mixer.music.get_pos() / 1000  # Get current position (seconds)
        if backward:
            new_position = max(0, current_position - seconds)
        else:
            new_position = current_position + seconds
        
        # Start from the new position using FFmpeg
        os.system(f"ffmpeg -ss {new_position} -i \"{file_path}\" -acodec copy temp.mp3 -y")
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()

    def toggle_mode(self):
        """Changes the mode."""
        if self.mode == 'Random':
            self.mode = 'Sequential'
        else:
            self.mode = 'Random'
        console.print(f"[blue]Mode changed:[/] {self.mode}")

    def toggle_mode2(self):
        """Changes mode 2."""
        if self.mode2 == 'Repeat':
            self.mode2 = 'Single Play'
        elif self.mode2 == 'Single Play':
            self.mode2 = 'All Play'
        elif self.mode2 == 'All Play':
            self.mode2 = 'Loop'
        else:
            self.mode2 = 'Repeat'
        console.print(f"[blue]Mode2 changed:[/] {self.mode2}")

    def set_folder_path(self):
        """Sets and saves the folder path."""
        new_path = Prompt.ask("Enter the file path (leave blank to keep current):", default=self.folder_path)
        if new_path:
            self.folder_path = new_path
            self.load_playlist()  # Load playlist when folder path is set
            self.save_settings()  # Save the new setting
        else:
            console.print("[yellow]Old file path is retained.[/]")  # Inform user when left blank

    def quit(self):
        """Exits the application."""
        pygame.mixer.quit()
        console.print("[red]Exiting the application...[/]")
        exit()

    def show_current_song_info(self):
        """Displays info about the current song."""
        if self.playlist:
            current_song = self.playlist[self.current_index]
            song_path = os.path.join(self.folder_path, current_song)
            audio = MP3(song_path)
            total_duration = audio.info.length  # Total song duration
            current_position = pygame.mixer.music.get_pos() / 1000  # Current position

            total_minutes, total_seconds = divmod(int(total_duration), 60)
            current_minutes, current_seconds = divmod(int(current_position), 60)

            song_info = (
                f"Song: {current_song}\n"
                f"Total Duration: {total_minutes:02}:{total_seconds:02}\n"
                f"Current Duration: {current_minutes:02}:{current_seconds:02}"
            )
            console.print(f"[yellow]- CURRENT SONG INFO -[/]\n{song_info}")
        else:
            console.print("[red]Playlist is empty![/]")

    def queue_song(self, song_index):
        """Queues the song."""
        if 0 <= song_index < len(self.playlist):
            # Allow adding the same song multiple times
            self.queue.append(song_index)
            console.print(f"[blue]Queued:[/] {self.playlist[song_index]}")
        else:
            console.print("[red]Invalid song number![/]")

    def remove_from_queue(self, song_index):
        """Removes the song from the queue."""
        if 0 <= song_index < len(self.playlist):  # Check if song index is valid
            if song_index in self.queue:
                self.queue.remove(song_index)
                console.print(f"[blue]Removed from queue:[/] {self.playlist[song_index]}")
            else:
                console.print("[red]Song not found in queue![/]")
        else:
            console.print("[red]Invalid song number![/]")

    def play_from_queue(self):
        """Plays the first song in the queue."""
        if self.queue:
            song_index = self.queue.pop(0)
            self.current_index = song_index
            self.play_song()
        else:
            console.print("[red]Queue is empty![/]")

    def adjust_volume(self, change):
        """Adjusts the volume level."""
        self.volume = max(0, min(1.0, self.volume + change))
        pygame.mixer.music.set_volume(self.volume)  # Set application volume
        console.print(f"[green]Volume level:[/] {self.volume * 10:.0f}")
    
    def show_queue(self):
        """Displays the songs in the queue."""
        if self.queue:
            table = Table(title="Song Queue")
            table.add_column("Index", justify="center")
            table.add_column("Song Name", justify="left")

            # Check if each index in the queue is valid
            for index in self.queue:
                if 0 <= index < len(self.playlist):
                    table.add_row(str(index + 1), self.playlist[index])
                else:
                    console.print(f"[red]Invalid song index: {index}[/]")  # Inform for invalid index

            console.print(table)
        else:
            console.print("[red]Queue is empty![/]")

def main():
    player = MusicPlayer()

    while True:
        clear_screen()  # Clear the screen
        console.print("[bold]    -  MP3 PLAYER  -[/]\n")
        scii_art()
        # Show mode states
        console.print(f"0 - Mode   (currently: {player.mode})")
        console.print(f"1 - Mode2  (Instant: {player.mode2})")

        choice = Prompt.ask("Make your selection")

        if choice == "0":
            player.toggle_mode()
        elif choice == "1":
            player.toggle_mode2()
        elif choice == "5":
            player.toggle_play_pause()
        elif choice == "4":
            player.previous_song()
        elif choice == "6":
            player.next_song()
        elif choice == "7":
            player.seek_backward(10)
        elif choice == "9":
            try:
                minutes = int(Prompt.ask("Which minute do you want to set the song to?"))
                player.seek_to_time(minutes)
            except ValueError:
                console.print("[red]Invalid minute![/]")
        elif choice == "3":
            player.show_playlist()
            console.print("Enter song number, queue with '-s {song number}' or remove from queue with '-d {song number}':")
            command = Prompt.ask("Enter command")
            if command.isdigit():
                song_index = int(command) - 1
                player.current_index = song_index
                player.play_song()
            elif command.startswith("-s "):
                try:
                    song_index = int(command.split(" ")[1]) - 1
                    player.queue_song(song_index)
                except ValueError:
                    console.print("[red]Invalid song number![/]")
            elif command.startswith("-d "):
                try:
                    song_index = int(command.split(" ")[1]) - 1
                    player.remove_from_queue(song_index)
                except ValueError:
                    console.print("[red]Invalid song number![/]")
            else:
                console.print("[red]Invalid command![/]")
        elif choice == "8":
            try:
                volume = int(Prompt.ask("Enter volume level (0-10)")) / 10
                player.adjust_volume(volume - player.volume)
            except ValueError:
                console.print("[red]Invalid volume level![/]")
        elif choice == "2":
            player.set_folder_path()
        elif choice in ["s", "S"]:
            player.show_queue()
        elif choice in ["i", "İ"]:
            player.show_current_song_info()
            Prompt.ask("Press any key to continue...")
        elif choice in ["q", "Q"]:
            player.quit()
        elif choice in ["h", "H", "Help", "help"]:
            show_help()
            Prompt.ask("Press any key to continue...")
        else:
            console.print("[red]Invalid selection![/]")

if __name__ == "__main__":
    main()
