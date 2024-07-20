import tkinter as tk
import tkinter.font as Font
import random
from PlayerManager import *
from GameManager import alphabet, weights

WIDTH, HEIGHT = 800, 600

class GUI(tk.Tk):
    def __init__(self, game_manager):
        super().__init__()
        self.title("WordBrawl")
        self.resizable(False, False)
        self.game_manager = game_manager

        self.option_add("*Frame.relief", "solid")
        self.option_add("*Frame.pack_propagate", False)
        self.option_add("*Label.justify", "center") #removed T
        self.option_add("*background", "white")

        OFFSETX = (self.winfo_screenwidth() - WIDTH) // 2
        OFFSETY = (self.winfo_screenheight() - HEIGHT) // 2
        self.geometry(f"{WIDTH}x{HEIGHT}+{OFFSETX}+{OFFSETY}")
    
        def _create_circle(root, x, y, r, o):
            return root.create_oval(x-r, y-r, x+r, y+r, fill = "white", outline = o, width = 3)
        tk.Canvas.create_circle = _create_circle

        self.pages = {
            "main_menu" : HomePage(self),
            "best_words" : BestWordsPage(self),
            "name_enter" : NameEnterPage(self),
            "result" : ResultPage(self),
            "gameplay" : GamePage(self)
        }

        self.current_page = self.pages["main_menu"]
    
    def tksleep(self, ms):
        var = tk.IntVar(self)
        self.after(ms, lambda: var.set(1))
        self.wait_variable(var)
    
    def switch_page(self, page_name):
        self.current_page.hide()
        self.current_page = self.pages[page_name]
        self.current_page.show()

        self.update_idletasks()

    def on_startup(self):
        self.current_page.hide()
        self.current_page = self.pages["main_menu"]
        self.current_page.show()

    def on_best_word(self):
        self.current_page.hide()
        self.current_page = self.pages["best_words"]
        self.current_page.show()

    def on_new_game(self):
        self.current_page.hide()
        self.current_page = self.pages["name_enter"]
        self.current_page.show()

    def on_new_round(self):
        self.current_page.hide()
        self.current_page = self.pages["gameplay"]
        self.current_page.show()

    def on_end_round(self):
        self.current_page.hide()
        self.current_page = self.pages["result"]
        self.current_page.show()   

class Page(tk.Frame):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.gui.update_idletasks()

    def hide(self):
        self.pack_forget()

    def handle_user_input(self, event):
        pass

class HomePage(Page):
    def __init__(self, gui):
        super().__init__(gui)
        self.pack_propagate(0)

        title = tk.Label(self, text="Word BRAWL", font=("Arial Bold", 75))
        title.pack(pady=(HEIGHT//3, 0))

        LinkedLabel(self, text = "New Game").on_click(lambda event: gui.on_new_game())
        LinkedLabel(self, text = "Best Words").on_click(lambda event: gui.on_best_word())

class BestWordsPage(Page):
    def __init__(self, gui):
        super().__init__(gui)
        self.pack_propagate(0)

        title = tk.Label(self, text="Best Words", font=("Arial Bold", 60))
        title.pack(pady=(HEIGHT // 6, 0))

        word_container = tk.Frame(self, bd=3, width=WIDTH//2, height=HEIGHT//2)
        word_container.pack(pady=10)
        word_container.pack_propagate(0)

        self.best_word_label = []
        for i in range(10):
            self.best_word_label.append(tk.Label(word_container, text = "-", font = ("Arial Bold", 16)))
            self.best_word_label[i].pack(expand = True)
        
        LinkedLabel(self, text = "BACK").on_click(lambda event: gui.on_startup())

    def show(self):
        best_words = self.gui.game_manager.file_manager.get_best_words()
        for idx, word in enumerate(best_words):
            self.best_word_label[idx].config(text = word)

        super().show()

class NameEnterPage(Page):
    def __init__(self, gui):
        super().__init__(gui)
        self.pack_propagate(0)

        title = tk.Label(self, text="ENTER YOUR NAME", font=("Arial Bold", 30))
        title.pack(pady=(HEIGHT // 3, 0))

        self.entry_val = tk.StringVar()
        self.entry_val.trace_add("write", self.capitalize)
        
        self.entry = tk.Entry(self, textvariable = self.entry_val, highlightthickness = 0, font = ("Arial", 20), width = 24)
        self.entry.pack(pady = 10, ipady = 2)
        self.entry.bind("<Return>", self.on_player_enter)

    def capitalize(self, *_):
        self.entry_val.set(self.entry_val.get().upper())

    def on_player_enter(self, *_):
        self.entry.configure(state = "disabled", cursor = "arrow")
        self.gui.tksleep(100)

        p1_name = self.entry_val.get()
        self.gui.game_manager.new_game(p1_name)

    def show(self):
        self.entry.configure(state = "normal")
        self.entry_val.set("")

        super().show()

class ResultPage(Page):
    def __init__(self, gui):
        super().__init__(gui)
        self.pack_propagate(0)

        self.message_label = tk.Label(self, font = ("Arial Bold", 75))
        self.message_label.pack(pady = (HEIGHT // 3, 0))
        LinkedLabel(self, text = "CONTINUE").on_click(lambda event: self.next_GUI())

    def next_GUI(self):
        GAME_OVER = self.gui.game_manager.is_game_over()

        if GAME_OVER:
            self.gui.on_best_word()
        else:
            self.gui.game_manager.new_round()

    def show(self):
        self.message_label.config(text = self.gui.game_manager.result_message)
        super().show()

class GamePage(Page):
    class HeadPanel(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.pack_propagate(0)

            ParentPanel = tk.Frame(self, width = 650, height = 65)
            ParentPanel.pack(side = "bottom")
            ParentPanel.pack_propagate(0)

            parent.health_bar = tk.Frame(ParentPanel, height = 35, bd = 3)
            parent.health_bar.pack(fill = "x", expand = True)
            parent.health_bar.pack_propagate(0)

            parent.health_player = tk.Frame(parent.health_bar, bg = "#C7B68B")
            parent.health_player.pack(side = "left", fill = "y") 
            parent.health_player.pack_propagate(0)

            parent.p1_label = tk.Label(parent.health_player, text="", font=("Arial Bold", 16), bg="#C7B68B")
            parent.p2_label = tk.Label(parent.health_bar, text="", font=("Arial Bold", 16))
        
            parent.win_canvas = tk.Canvas(ParentPanel, width = 650, height = 30, highlightthickness = 0)
            parent.win_canvas.pack(side = "left")

            parent.win_circles = {
                "Player 1" : [None, None, None], 
                "Player 2" : [None, None, None]
            }

            for i in range(3):
                POS = 15 + 25 * i
                parent.win_circles["Player 1"][i] = parent.win_canvas.create_circle(x=POS, y =15, r=5, o="black")
                parent.win_circles["Player 2"][i] = parent.win_canvas.create_circle(x=650-POS, y=15, r=5, o="black")

    class WordPanel(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.pack_propagate(0)

            parent.AttackButton = tk.Canvas(self, width = 60, height = 60, cursor = "hand")
            parent.AttackButton.configure(bd = 0, highlightthickness = 0)
            parent.AttackButton.pack(side = "right", anchor = "s")
            parent.AttackButton.bind("<ButtonRelease-1>", lambda event: parent.on_submit_word())
  
            parent.AttackCircle = parent.AttackButton.create_circle(x = 30, y = 30, r = 25, o = "#E8E9E8")
            parent.AttackText = parent.AttackButton.create_text(30, 30, text = "GO", font = "Arial 20 bold", fill = "#E8E9E8")
            
            parent.LabelWord = tk.Label(self)
            parent.LabelWord.font = Font.Font(family = "Arial Bold", size = 60)
            parent.LabelWord.config(font = parent.LabelWord.font)
            parent.LabelWord.pack(side = "left", anchor = "s", fill = "x", expand = True)

    class LttrPanel(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.pack_propagate(0)

            OFFSET_BY_HIGHLIGHT = 3 * 2
            LetterContainer = tk.Frame(self, width = 315, height = 300 + OFFSET_BY_HIGHLIGHT)
            LetterContainer.pack(side = "left")
            LetterContainer.pack_propagate(0)

            parent.LetterBoxes = []
            parent.SelectedBoxes = [] #transfer gamemanager

            letter_grid = tk.Text(LetterContainer, highlightthickness = 0, relief = "solid")
            letter_grid.config(selectbackground = "white", inactiveselectbackground = "white")
            letter_grid.config(wrap = "char", state = "disabled", cursor = "arrow")
            letter_grid.tag_configure("align")
            letter_grid.pack(fill = "both", expand = True)
            letter_grid.pack_propagate(0)

            for id in range(25):
                letter_box = LinkedButton(letter_grid, text = "", id = id)
                letter_box.button_label.config(font = ("Arial", 25))
                letter_box.config(width = 60, height = 60, highlightthickness = 3, highlightbackground = "white")
                letter_box.on_click(lambda event, l=letter_box: parent.on_letter_release(l))

                parent.LetterBoxes.append(letter_box)
                letter_grid.window_create("0.0", window = letter_box)
                letter_grid.tag_add("align", "1.0", "end")

    class ShopPanel(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.pack_propagate(0)

            shop_container = tk.Frame(self, bd = 3, width = 315, height = 300)
            shop_container.pack(side = "right", padx = 3, pady = 3)
            shop_container.pack_propagate(0)

            coin_panel = tk.Frame(shop_container, width = 270, height = 50)
            coin_panel.pack(fill = "x", padx = 30, pady = (50, 0))
            coin_panel.pack_propagate(0)

            tk.Label(coin_panel, text = "Coins: ", font = ("Arial Bold", 20)).pack(side = "left", padx = (10, 0))
            parent.coin_num = tk.Label(coin_panel, font = ("Arial", 20))
            parent.coin_num.pack(side = "left")

            shop_items = {
                "Replace." : lambda event: parent.gui.game_manager.buy_replace(), 
                "Wildcard." : lambda event:  parent.gui.game_manager.buy_wildcard(),
                "Powerup." : lambda event: parent.gui.game_manager.buy_powerup()
            }

            for option, trigger in shop_items.items():
                option_panel = tk.Frame(shop_container, width = 270, height = 50)
                option_panel.pack(fill = "x", padx = 30)
                option_panel.pack_propagate(0)

                buy_button = LinkedButton(option_panel, text = "BUY", width = 50, height = 30)
                buy_button.button_label.config(font = ("Arial Bold", 16))
                buy_button.pack(side = "left", padx = 10)
                buy_button.on_click(trigger)

                PRICE = 10
                tk.Label(option_panel, text = option, font = ("Arial Bold", 20)).pack(side = "left")
                tk.Label(option_panel, text = f"{PRICE} Coins", font = ("Arial", 20)).pack(side = "left")

    class WaitingPanel(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            self.pack_propagate(0)

            parent.waiting_text = tk.Label(self, font = ("Arial Bold", 30), relief = "solid")
            parent.waiting_text.config(width = 650, height = 300, bd = 3)
            parent.waiting_text.pack(pady = 30, fill = "y", expand = True, anchor = "center")

    def __init__(self, gui):
        super().__init__(gui)

        self.HP = self.HeadPanel(self)
        self.WP = self.WordPanel(self)
        self.LP = self.LttrPanel(self)
        self.SP = self.ShopPanel(self)
        self.WaitP = self.WaitingPanel(self)

        self.HP.grid(row = 0, column = 0, columnspan = 2, padx = 75, sticky = "nsew")
        self.WP.grid(row = 1, column = 0, columnspan = 2, padx = 75, sticky = "nsew")
        self.LP.grid(row = 2, column = 0, padx = (75, 0), sticky = "nsew")
        self.SP.grid(row = 2, column = 1, padx = (0, 75), sticky = "nsew")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 3)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
    
    def update_letter_grid(self):
        if (self.gui.game_manager.letter_grid_array == None):
            raise LookupError
            self.gui.game_manager.letter_grid_array = random.choices(alphabet, weights, k = 25)
        
        for index, letter in enumerate(self.gui.game_manager.letter_grid_array):
            self.LetterBoxes[index].set_text(letter)

        self.gui.tksleep(100)

    def update_health(self):
        self.health_player.config(width = 650 * self.gui.game_manager.Player1.health // 100)

    def update_coins(self):
        self.coin_num.config(text = self.gui.game_manager.Player1.coins)

    def update_word(self):
        self.LabelWord.config(text = self.gui.game_manager.word)

        size = self.LabelWord.font.actual("size")
        WIDGETWIDTH = self.LabelWord.winfo_width() - 30
        while size < 60 and self.LabelWord.font.measure(self.gui.game_manager.word) < WIDGETWIDTH:
            size += 1
            self.LabelWord.font.config(size = size)
        while size > 20 and self.LabelWord.font.measure(self.gui.game_manager.word) > WIDGETWIDTH:
            size -= 1
            self.LabelWord.font.config(size = size)

    def on_letter_release(self, letter_box):
        word = self.gui.game_manager.get_word()

        if letter_box in self.SelectedBoxes:
            index = self.SelectedBoxes.index(letter_box)
            for letter_box in self.SelectedBoxes[index:]:
                letter_box.activate()
            word = word[:index]
            self.SelectedBoxes = self.SelectedBoxes[:index]
        else:
            letter_box.deactivate()
            word = word + letter_box.get_text()
            self.SelectedBoxes.append(letter_box)

        self.gui.game_manager.set_word(word)

        if self.gui.game_manager.is_valid_word(): # transfer to game_manager
            self.AttackButton.itemconfig(self.AttackCircle, fill = "black", outline = "black")
            self.AttackButton.itemconfig(self.AttackText, fill = "white")
        else:
            self.AttackButton.itemconfig(self.AttackCircle, fill = "white", outline = "#E8E9E8")
            self.AttackButton.itemconfig(self.AttackText, fill = "#E8E9E8")
        
    def on_submit_word(self):
        if self.gui.game_manager.is_valid_word():
            word = self.LabelWord.cget("text")

            self.AttackButton.itemconfig(self.AttackCircle, fill = "white", outline = "#E8E9E8")
            self.AttackButton.itemconfig(self.AttackText, fill = "#E8E9E8")

            base_damage = self.gui.game_manager.get_base_damage()
            for letter_box in self.SelectedBoxes:
                if letter_box.cget("bg") == "#C7B68B":
                    base_damage += 1
            
            self.gui.game_manager.set_base_damage(base_damage)

            self.SelectedBoxes.sort(key = lambda x: self.LetterBoxes.index(x), reverse = True)
            # First Letter Grid Index Destroyed First

            for letter in word:
                bonus_damage = int(1 / weights[alphabet.index(letter)]) // 2
                total_damage = (base_damage + bonus_damage) * self.gui.game_manager.damage_multiplier

                word = word.replace(letter, f" +{total_damage} ", 1)
                self.gui.game_manager.set_word(word)

                self.gui.game_manager.earn_coins(base_damage)
                self.gui.game_manager.send_damage(total_damage)

                self.SelectedBoxes[0].activate()
                letterbox_to_remove = self.SelectedBoxes.pop(0).id
                self.gui.game_manager.pop_letterbox(letterbox_to_remove)

                self.gui.tksleep(100)

            self.gui.game_manager.on_submit_word(word)
            print("sent")

    def show_gameplay(self):
        # self.update_letter_grid()
        
        self.LP.grid(row = 2, column = 0, padx = (75, 0), sticky = "nsew")
        self.SP.grid(row = 2, column = 1, padx = (0, 75), sticky = "nsew")
        self.WaitP.grid_forget()

    def show_waiting(self):
        self.LP.grid_forget()
        self.SP.grid_forget()
        self.WaitP.grid(row = 2, column = 0, columnspan = 2, padx = 75, sticky = "nsew")
        self.waiting_text.configure(text = self.gui.game_manager.Player2.name + " is guessing")

    def show(self):
        self.p1_label.config(text = self.gui.game_manager.Player1.name)
        self.p2_label.config(text = self.gui.game_manager.Player2.name)
        
        self.p1_label.pack(side="left", padx=3)
        self.p2_label.pack(side="right", padx=3)
        
        for i in range(3):
            win_circle = self.win_circles["Player 1"][i]
            win_count = self.gui.game_manager.Player1.wins
            fill_color = "black" if (i < win_count) else "white"
            self.win_canvas.itemconfig(win_circle, fill=fill_color)

            win_circle = self.win_circles["Player 2"][i]
            win_count = self.gui.game_manager.Player2.wins
            fill_color = "black" if (i < win_count) else "white"
            self.win_canvas.itemconfig(win_circle, fill=fill_color)

        self.update_coins()
        self.update_health()

        self.SelectedBoxes.clear()
        self.gui.tksleep(100)

        if self.gui.game_manager.active_player == self.gui.game_manager.Player1:
            self.show_gameplay()
            self.gui.game_manager.socket.stop_receiving()
        else:
            self.show_waiting()
            self.gui.game_manager.socket.start_receiving()
        super().show()

class LinkedLabel(tk.Label):
    def __init__(self, parent, text):
        tk.Label.__init__(self, parent, cursor = "hand1")
        self.config(text = text, font = ("Arial Bold", 20))
        self.pack(pady = 10)

    def on_click(self, func):
        self.bind("<ButtonRelease-1>", func)

class LinkedButton(tk.Frame):
    def __init__(self, parent, text = "", id = None, is_bonus = False, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.pack_propagate(0)

        self.id = id
        self.is_bonus = is_bonus
        color = "#C7B68B" if self.is_bonus else "white"

        self.button_label = tk.Label(self, text = text, bg = color)
        self.button_label.pack(fill = "both", expand = True, padx = 3, pady = 3)

        self.activate()

    def activate(self):
        self.config(bg = "black")
        self.button_label.config(fg = "black")
        self.button_label.config(cursor = "hand1")

    def deactivate(self):
        self.config(bg = "#E8E9E8")
        self.button_label.config(fg = "#E8E9E8")
        self.button_label.config(cursor = "arrow")

    def on_click(self, func):
        self.button_label.bind("<ButtonRelease-1>", func)

    def set_text(self, text):
        self.button_label.config(text = text)

    def get_text(self):
        return self.button_label.cget("text")
