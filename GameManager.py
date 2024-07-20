import random, nltk, hashlib
from PlayerManager import Player

dictionary = set(word.upper() for word in nltk.FreqDist(nltk.corpus.brown.words()))
alphabet, weights = [], []

constructor = {
    1 : ['A', 'E', 'I', 'O', 'U'],
    2 : ['D', 'G', 'L', 'N', 'R', 'S', 'T'],
    3 : ['B', 'C', 'F', 'H', 'M', 'P'],
    4 : ['V', 'W', 'Y'],
    5 : ['J', 'K', 'Q'],
    6 : ['X', 'Z']
}

for key, val in constructor.items():
    for letter in val:
        alphabet.append(letter)
        weights.append(1/key)

SHOP_PRICE = 10

class GameManager:
    def __init__(self, gui_manager = None, socket = None, file_manager = None):
        self.Player1 = None
        self.Player2 = None
        self.active_player = None
        self.idle_player = None

        self.word = ""
        self.damage_multiplier = 1
        self.letter_grid_array = []

        self.gui_manager = gui_manager #should be gameplay_gui_manager
        self.socket = socket
        self.file_manager = file_manager

    def new_game(self, p1_name):
        self.socket.opponent.sendall(p1_name.encode())
        p2_name = self.socket.opponent.recv(1024).decode()

        self.Player1 = Player(p1_name)
        self.Player2 = Player(p2_name)

        p1_hash = int(hashlib.sha256(p1_name.encode('utf-8')).hexdigest(), base=16)
        p2_hash = int(hashlib.sha256(p2_name.encode('utf-8')).hexdigest(), base=16)

        if p1_hash > p2_hash:
            self.active_player = self.Player1
            self.idle_player = self.Player2

        if p1_hash < p2_hash:
            self.active_player = self.Player2
            self.idle_player = self.Player1

        if p1_hash == p2_hash:
            raise Exception

        self.new_round()

    def new_round(self):
        self.Player1.health = 50
        self.Player1.base_damage = 2
        self.Player1.coins = 0

        self.Player2.health = 50
        self.Player2.base_damage = 2
        self.Player2.coins = 0

        self.letter_grid_array = random.choices(alphabet, weights, k = 25)
        self.gui_manager.update_letter_grid()

        self.switch_turns()
        self.gui_manager.gui.on_new_round()
    
    def pop_letterbox(self, index, new_letter = None):
        if new_letter == None:
            new_letter = random.choices(alphabet, weights, k = 1)[0]

        self.letter_grid_array.pop(index)
        self.letter_grid_array.insert(0, new_letter)
        self.gui_manager.update_letter_grid()

    def buy_replace(self):
        self.spend_coins(SHOP_PRICE)

        for index in range(25):
            self.pop_letterbox(index)
            
        if self.active_player.coins < 0:
            self.active_player.coins = 0
            self.gui_manager
            self.socket.send_operator("Swap", "".join(self.letter_grid_array))

            self.switch_turns()
    
    def buy_wildcard(self):
        if self.active_player.coins < SHOP_PRICE:
            return

        self.spend_coins(SHOP_PRICE)

        random_index = random.choice([i for i in range(25) if self.letter_grid_array[i] != '?'])
        self.letter_grid_array[random_index] = '?'
        self.gui_manager.update_letter_grid()

        wildcard = self.gui_manager.LetterBoxes[random_index]
        if wildcard in self.gui_manager.SelectedBoxes:
            wildcard_index = self.gui_manager.SelectedBoxes.index(wildcard)
            self.set_word(self.word[:wildcard_index] + '?' + self.word[wildcard_index + 1:])

    def buy_powerup(self):
        if self.active_player.coins < SHOP_PRICE:
            return
        
        self.spend_coins(SHOP_PRICE)

        self.damage_multiplier += 1
    
    def earn_coins(self, amount):
        self.active_player.coins += amount
        self.gui_manager.update_coins()

    def spend_coins(self, amount):
        self.active_player.coins -= amount
        self.gui_manager.update_coins()

    def send_damage(self, damage):
        self.active_player.health += damage
        self.idle_player.health -= damage
        self.gui_manager.update_health()

    def on_submit_word(self, word): # remove word
        self.file_manager.update_best_words(word)
        self.socket.send_operator("Swap", "".join(self.letter_grid_array))
        self.switch_turns()

        if self.Player1.health >= 100:
            self.win_routine(self.Player1) #transfer win_routine to here
        
        if self.Player2.health >= 100:
            self.win_routine(self.Player2)

    def on_swap(self, new_letter_grid_array):
        """for index, letter in enumerate(reversed(new_letter_grid_array)):
            self.gui_manager.LetterBoxes[index].set_text(letter)"""
        
        new_letter_grid_array = list(new_letter_grid_array)
        for index, letter in enumerate(new_letter_grid_array):
            if letter == "?":
                new_letter_grid_array[index] = random.choices(alphabet, weights, k = 1)[0]
        
        self.letter_grid_array = new_letter_grid_array
        self.gui_manager.update_letter_grid()
        self.switch_turns()

        if self.Player1.health >= 100:
            self.win_routine(self.Player1) #transfer win_routine to here
        
        if self.Player2.health >= 100:
            self.win_routine(self.Player2)

    def get_word(self):
        return self.word

    def set_word(self, word):
        self.word = self.match_wildcard(word)
        self.socket.send_operator("Word", self.word)
        self.gui_manager.update_word() 

    def match_wildcard(self, word):
        if "?" in word:
            for letter in alphabet:
                temp = word.replace("?", letter, 1)
                temp = self.match_wildcard(temp)
                
                if temp in dictionary:
                    return temp
        return word

    def is_valid_word(self):
        COND1 = len(self.word) > 2
        COND2 = self.word in dictionary

        return COND1 and COND2
    
    def get_base_damage(self):
        return self.active_player.base_damage
    
    def set_base_damage(self, value):
        self.active_player.base_damage = value

    def switch_turns(self):
        self.set_word("")
        self.damage_multiplier = 1

        self.active_player, self.idle_player = self.idle_player, self.active_player

        if self.Player1 == self.active_player:
            self.gui_manager.show_gameplay()
            self.socket.stop_receiving()
        else:
            self.gui_manager.show_waiting()
            self.socket.start_receiving()

    def is_game_over(self):
        return self.Player1.wins == 3 or self.Player2.wins == 3

    def win_routine(self, player):
        WIN_MSG = ["CONGRATS!", "WINNER!", "YOU WON!"]
        LOSE_MSG = ["LOZER!", "KAWAWA!", "YOU LOST!"]

        if player == self.Player1:
            self.result_message = WIN_MSG[self.Player1.wins]
        else:
            self.result_message = LOSE_MSG[self.Player2.wins]
        
        player.wins += 1
        self.gui_manager.gui.on_end_round()