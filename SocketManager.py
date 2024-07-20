from socket import socket, AF_INET, SOCK_STREAM

class Socket:
    def __init__(self, game_manager):
        self.HOST = '127.0.0.1'
        #self.HOST = '192.168.86.190'
        self.PORT = 65432

        self.game_manager = game_manager
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.opponent = None

    def start_socket(self):
        pass

    def close_socket(self):
        pass

    def send_operator(self, event_key, event_value):
        event_constructor = "{}::{}::".format(event_key, event_value)
        self.opponent.sendall(event_constructor.encode())

    def start_receiving(self):
        self.open_receiving.set()

    def stop_receiving(self):
        self.open_receiving.clear()

    def recv_thread(self):
        data = ""
        while True:
            self.open_receiving.wait()
            data += self.opponent.recv(1024).decode()

            if not data: 
                self.close_socket()
            print(data)
            '''
            protocol is <key>::<val>::
            data has two possible keys
            
            1. Word - after pressing LetterBox / WildCard
            2. Swap - replaces Letter_Grid and switches players
            '''

            while data.count("::") >= 2:
                event_key, event_value, data = data.split("::", 2)
                if "Word" in event_key:
                    if not event_value:
                        event_value = ""
                    if "+" in event_value:
                        latest_dmg_index = event_value.rindex("+") + 1
                        damage = event_value[latest_dmg_index: latest_dmg_index + 2]

                        self.game_manager.send_damage(int(damage))
                    self.game_manager.word = event_value.replace("+", "−")
                    self.game_manager.gui_manager.update_word() 
                    # using set_word causes feedback loop

                if "Swap" in event_key: # event_key == swap
                    self.game_manager.on_swap(event_value)