from GameManager import GameManager
from FileManager import FileManager
from SocketManager import Socket
from GuiManager import GUI
import threading

def start_socket(self):
    self.socket.connect((self.HOST, self.PORT))
    self.opponent = self.socket

    self.open_receiving = threading.Event()
    self.socket_thread = threading.Thread(target = self.recv_thread)
    self.socket_thread.daemon = True
    self.socket_thread.start()

def close_socket(self):
    self.socket.close()

if __name__ == "__main__":
    file_manager = FileManager()
    game_manager = GameManager()

    socket = Socket(game_manager)
    socket.start_socket = start_socket
    socket.close_socket = close_socket

    gui_manager = GUI(game_manager)
    game_manager.gui_manager = gui_manager.pages['gameplay']
    game_manager.socket = socket
    game_manager.file_manager = file_manager

    socket.start_socket(socket)

    gui_manager.on_startup()
    gui_manager.mainloop()

    socket.close_socket(socket)
