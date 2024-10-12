#ONAYLANDI ANCAK EKSİĞİ VAR
import time
import os
import json
import pygame
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from mutagen.mp3 import MP3

# Pygame başlat
pygame.mixer.init()

# Rich konsol
console = Console()

# Ayar dosyası
settings_file = "ConsolMp.json"

def clear_screen():
    """Ekranı temizler."""
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
    # Ekran boyutunu al
    print(art)

def show_help():
    help_text = """
      -  MENÜ  -
0 - Mod   (o an: Karışık)
1 - Mod2  (Anlık: Repeat)
5 - Şarkıyı Durdur/Başlat
4 - Önceki Şarkıya Geç
6 - Sonraki Şarkıya Geç
7 - 10 sn Geri Al
9 - 10 sn İleri Al
3 - Çalma Listesini Göster
8 - Ses Seviyesini Ayarla (0-10)
2 - Dosya Yolu Ayarla
h - Şarkı Hakkında Bilgi
q - Çıkış
    """
    console.print(help_text)

class MusicPlayer:
    def __init__(self):
        
        self.playlist = []
        self.current_index = 0
        self.mode = 'Karışık'  # Başlangıç modu
        self.mode2 = 'Repeat'  # Başlangıç mod2
        self.is_playing = False
        self.volume = 0.5  # Ses seviyesi
        self.folder_path = ""  # Klasör yolu başlangıçta boş
        self.load_settings()  # Ayarları yükle
        self.load_playlist()  # Playlisti yükle
        self.queue = []  # Şarkı sırası
        


    def load_settings(self):
        """Ayar dosyasından dosya yolunu yükler."""
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as file:
                settings = json.load(file)
                self.folder_path = settings.get("folder_path", "")
                console.print(f"[green]Ayarlar yüklendi:[/] Klasör yolu: {self.folder_path}")
        else:
            console.print("[yellow]Ayar dosyası bulunamadı. Yeni yol ayarlayın.[/]")

    def save_settings(self):
        """Ayarları dosyaya kaydeder."""
        settings = {
            "folder_path": self.folder_path
        }
        with open(settings_file, 'w') as file:
            json.dump(settings, file)
            console.print("[green]Ayarlar kaydedildi.[/]")

    def load_playlist(self):
        """Belirtilen klasördeki MP3 dosyalarını yükler."""
        if self.folder_path:
            self.playlist = [f for f in os.listdir(self.folder_path) if f.endswith('.mp3')]
            console.print(f"[green]Çalma listesi yüklendi:[/] {len(self.playlist)} şarkı bulundu.")
        else:
            console.print("[red]Klasör yolu ayarlanmamış![/]")

    def show_playlist(self):
        """Çalma listesini gösterir."""
        table = Table(title="Çalma Listesi")
        table.add_column("Index", justify="center")
        table.add_column("Şarkı Adı", justify="left")

        for index, song in enumerate(self.playlist):
            table.add_row(str(index + 1), song)

        console.print(table)

    def play_song(self):
        """Şarkıyı çalar."""
        if self.playlist:
            song_path = os.path.join(self.folder_path, self.playlist[self.current_index])
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.volume)  # Ses seviyesini ayarla
            pygame.mixer.music.play()
            self.is_playing = True
            self.show_current_song_info()  # Çalan şarkı hakkında bilgi göster
        else:
            console.print("[red]Çalma listesi boş![/]")

    def toggle_play_pause(self):
        """Şarkıyı duraklatır veya devam ettirir."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            console.print("[yellow]Şarkı duraklatıldı.[/]")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            console.print("[green]Şarkı devam ediyor.[/]")

    def next_song(self):
        """Sonraki şarkıya geçer."""
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()
        else:
            console.print("[red]Çalma listesi boş![/]")

    def previous_song(self):
        """Önceki şarkıya geçer."""
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()
        else:
            console.print("[red]Çalma listesi boş![/]")

    def seek_forward(self, seconds):
        """Şarkıyı belirtilen saniye kadar ileri alır."""
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # Mevcut zamanı saniye cinsinden al
            new_time = current_time + seconds
            pygame.mixer.music.set_pos(new_time)
            console.print(f"[green]Şarkı {seconds} saniye ileri alındı.[/]")

    def seek_backward(self, seconds):
        """Şarkıyı belirtilen saniye kadar geri alır."""
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # Mevcut zamanı saniye cinsinden al
            new_time = max(0, current_time - seconds)  # Zamanı 0'ın altına düşmemesi için sınırla
            pygame.mixer.music.set_pos(new_time)
            console.print(f"[green]Şarkı {seconds} saniye geri alındı.[/]")  

    def seek_to_time(self, minutes):
        """Şarkıyı belirtilen dakikaya ayarlar."""
        if self.is_playing:
            current_pos = pygame.mixer.music.get_pos() / 1000  # Mevcut pozisyonu saniye cinsinden al
            new_pos = minutes * 60  # Dakikayı saniyeye çevir
            
            # FFmpeg kullanmadan sadece mevcut ses çalarak konum ayarlama
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=new_pos)
            
            console.print(f"[green]Şarkı {minutes} dakikaya ayarlandı.[/]")
        else:
            console.print("[red]Şarkı çalmıyor![/]")

    def ffmpeg_seek(self, file_path, seconds, backward=False):
        """Şarkıyı FFmpeg ile ileri veya geri sarar."""
        current_position = pygame.mixer.music.get_pos() / 1000  # Mevcut pozisyonu alır (saniye)
        if backward:
            new_position = max(0, current_position - seconds)
        else:
            new_position = current_position + seconds
        
        # FFmpeg ile yeni pozisyondan başlat
        os.system(f"ffmpeg -ss {new_position} -i \"{file_path}\" -acodec copy temp.mp3 -y")
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()

    def toggle_mode(self):
        """Modu değiştirir."""
        if self.mode == 'Karışık':
            self.mode = 'Sıralı'
        else:
            self.mode = 'Karışık'
        console.print(f"[blue]Mod değiştirildi:[/] {self.mode}")

    def toggle_mode2(self):
        """Mod 2'yi değiştirir."""
        if self.mode2 == 'Repeat':
            self.mode2 = 'Single Play'
        elif self.mode2 == 'Single Play':
            self.mode2 = 'All Play'
        elif self.mode2 == 'All Play':
            self.mode2 = 'Loop'
        else:
            self.mode2 = 'Repeat'
        console.print(f"[blue]Mod2 değiştirildi:[/] {self.mode2}")

    def set_folder_path(self):
        """Klasör yolunu ayarlar ve kaydeder."""
        new_path = Prompt.ask("Dosya yolunu girin (boş bırakmak mevcut yolu korur):", default=self.folder_path)
        if new_path:
            self.folder_path = new_path
            self.load_playlist()  # Klasör yolu ayarlandığında playlisti yükle
            self.save_settings()  # Yeni ayarı kaydet
        else:
            console.print("[yellow]Eski dosya yolu korunuyor.[/]")  # Kullanıcı boş bıraktığında bilgi ver

    def quit(self):
        """Uygulamadan çıkar."""
        pygame.mixer.quit()
        console.print("[red]Uygulamadan çıkılıyor...[/]")
        exit()

    def show_current_song_info(self):
        """Çalan şarkı hakkında bilgi gösterir."""
        if self.playlist:
            current_song = self.playlist[self.current_index]
            song_path = os.path.join(self.folder_path, current_song)
            audio = MP3(song_path)
            total_duration = audio.info.length  # Toplam şarkı süresi
            current_position = pygame.mixer.music.get_pos() / 1000  # Şu anki pozisyon

            total_minutes, total_seconds = divmod(int(total_duration), 60)
            current_minutes, current_seconds = divmod(int(current_position), 60)

            song_info = (
                f"Şarkı: {current_song}\n"
                f"Toplam Süre: {total_minutes:02}:{total_seconds:02}\n"
                f"Mevcut Süre: {current_minutes:02}:{current_seconds:02}"
            )
            console.print(f"[yellow]- ÇALAN ŞARKI HAKKINDA BİLGİ -[/]\n{song_info}")
        else:
            console.print("[red]Çalma listesi boş![/]")


    def queue_song(self, song_index):
        """Şarkıyı sıraya alır."""
        if 0 <= song_index < len(self.playlist):
            # Aynı şarkıyı birden fazla kez eklemeye izin verir
            self.queue.append(song_index)
            console.print(f"[blue]Sıraya alındı:[/] {self.playlist[song_index]}")
        else:
            console.print("[red]Geçersiz şarkı numarası![/]")

    def remove_from_queue(self, song_index):
        """Kuyruktaki şarkıyı çıkarır."""
        if 0 <= song_index < len(self.playlist):  # Şarkı indeksinin geçerli olup olmadığını kontrol et
            if song_index in self.queue:
                self.queue.remove(song_index)
                console.print(f"[blue]Sıradan çıkarıldı:[/] {self.playlist[song_index]}")
            else:
                console.print("[red]Şarkı sırada bulunmuyor![/]")
        else:
            console.print("[red]Geçersiz şarkı numarası![/]")


    def play_from_queue(self):
        """Kuyruktaki ilk şarkıyı çalar."""
        if self.queue:
            song_index = self.queue.pop(0)
            self.current_index = song_index
            self.play_song()
        else:
            console.print("[red]Kuyruk boş![/]")


    def adjust_volume(self, change):
        """Ses seviyesini ayarlar."""
        self.volume = max(0, min(1.0, self.volume + change))
        pygame.mixer.music.set_volume(self.volume)  # Uygulama sesini ayarla
        console.print(f"[green]Ses seviyesi:[/] {self.volume * 10:.0f}")
    
    def show_queue(self):
        """Kuyruktaki şarkıları gösterir."""
        if self.queue:
            table = Table(title="Şarkı Kuyruğu")
            table.add_column("Index", justify="center")
            table.add_column("Şarkı Adı", justify="left")

            # Kuyruktaki her indeksin geçerli olduğunu kontrol edin
            for index in self.queue:
                if 0 <= index < len(self.playlist):
                    table.add_row(str(index + 1), self.playlist[index])
                else:
                    console.print(f"[red]Geçersiz şarkı indeksi: {index}[/]")  # Geçersiz indeks durumunda bilgi verir

            console.print(table)
        else:
            console.print("[red]Kuyruk boş![/]")
        
            


def main():
    player = MusicPlayer()

    while True:
        clear_screen()  # Ekranı temizle
        console.print("[bold]    -  MP3 PLAYER  -[/]\n")
        scii_art()
        # Mod durumlarını göster
        console.print(f"0 - Mod   (o an: {player.mode})")
        console.print(f"1 - Mod2  (Anlık: {player.mode2})")

        choice = Prompt.ask("Seçiminizi yapın")

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
                minutes = int(Prompt.ask("Şarkıyı kaçıncı dakikaya ayarlamak istersiniz?"))
                player.seek_to_time(minutes)
            except ValueError:
                console.print("[red]Geçersiz dakika![/]")
        elif choice == "3":
            player.show_playlist()
            console.print("Şarkı numarasını girin, '-s {şarkı numarası}' ile sıraya alın veya '-d {şarkı numarası}' ile sıradan çıkarın:")
            command = Prompt.ask("Komut girin")
            if command.isdigit():
                song_index = int(command) - 1
                player.current_index = song_index
                player.play_song()
            elif command.startswith("-s "):
                try:
                    song_index = int(command.split(" ")[1]) - 1
                    player.queue_song(song_index)
                except ValueError:
                    console.print("[red]Geçersiz şarkı numarası![/]")
            elif command.startswith("-d "):
                try:
                    song_index = int(command.split(" ")[1]) - 1
                    player.remove_from_queue(song_index)
                except ValueError:
                    console.print("[red]Geçersiz şarkı numarası![/]")
            else:
                console.print("[red]Geçersiz komut![/]")
        elif choice == "8":
            try:
                volume = int(Prompt.ask("Ses seviyesini girin (0-10)")) / 10
                player.adjust_volume(volume - player.volume)
            except ValueError:
                console.print("[red]Geçersiz ses seviyesi![/]")
        elif choice == "2":
            player.set_folder_path()
        elif choice in ["s", "S"]:
            player.show_queue()
        elif choice in ["i", "İ"]:
            player.show_current_song_info()
            Prompt.ask("Devam etmek için bir tuşa basın...")
        elif choice in ["q", "Q"]:
            player.quit()
        elif choice in ["h", "H", "Help", "help"]:
            show_help()
            Prompt.ask("Devam etmek için bir tuşa basın...")
        else:
            console.print("[red]Geçersiz seçim![/]")

if __name__ == "__main__":
    main()
