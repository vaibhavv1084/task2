import os
import sys
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QFileDialog, QMessageBox

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(200, 200, 400, 350)

        pygame.mixer.init()

        self.playlist = []
        self.current_track_index = -1

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.playlist_box = QListWidget()
        layout.addWidget(self.playlist_box)

        play_btn = QPushButton("Play")
        play_btn.clicked.connect(self.play_music)
        layout.addWidget(play_btn)

        pause_btn = QPushButton("Pause")
        pause_btn.clicked.connect(self.pause_music)
        layout.addWidget(pause_btn)

        stop_btn = QPushButton("Stop")
        stop_btn.clicked.connect(self.stop_music)
        layout.addWidget(stop_btn)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.next_music)
        layout.addWidget(next_btn)

        prev_btn = QPushButton("Previous")
        prev_btn.clicked.connect(self.prev_music)
        layout.addWidget(prev_btn)

        add_btn = QPushButton("Add Song")
        add_btn.clicked.connect(self.add_song)
        layout.addWidget(add_btn)

        remove_btn = QPushButton("Remove Song")
        remove_btn.clicked.connect(self.remove_song)
        layout.addWidget(remove_btn)

        central_widget.setLayout(layout)

    def add_song(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Add Song", "", "MP3 Files (*.mp3)")
        if file_path:
            self.playlist.append(file_path)
            self.playlist_box.addItem(os.path.basename(file_path))

    def remove_song(self):
        selected_song_index = self.playlist_box.currentRow()
        if selected_song_index != -1:
            self.playlist.pop(selected_song_index)
            self.playlist_box.takeItem(selected_song_index)

    def play_music(self):
        if self.playlist:
            if self.playlist_box.currentRow() != -1:
                self.current_track_index = self.playlist_box.currentRow()
            else:
                self.current_track_index = 0
            self.load_music(self.playlist[self.current_track_index])
            pygame.mixer.music.play()

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()

    def next_music(self):
        if self.playlist and self.current_track_index < len(self.playlist) - 1:
            self.current_track_index += 1
            self.load_music(self.playlist[self.current_track_index])
            pygame.mixer.music.play()

    def prev_music(self):
        if self.playlist and self.current_track_index > 0:
            self.current_track_index -= 1
            self.load_music(self.playlist[self.current_track_index])
            pygame.mixer.music.play()

    def load_music(self, track):
        pygame.mixer.music.load(track)
        self.playlist_box.setCurrentRow(self.current_track_index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
