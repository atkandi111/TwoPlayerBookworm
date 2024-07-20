from GameManager import GameManager
from FileManager import FileManager
from SocketManager import Socket
from GuiManager import GUI

file_manager = FileManager()
game_manager = GameManager()
socket = Socket(game_manager)
gui_manager = GUI(game_manager)
game_manager.gui_manager = gui_manager
gui_manager.on_startup()

# main.py for server and another main.py for client