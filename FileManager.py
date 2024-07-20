import os

class FileManager:
    PATH = os.path.join(os.getcwd(), "Records.txt")

    def __init__(self):
        self.best_words = self.get_best_words()

    def get_best_words(self):
        if os.path.isfile(self.PATH):
            with open(self.PATH, 'r') as file:
                return [line.strip() for line in file]
        else:
            return []

    def update_best_words(self, new_word):
        temp = sorted(self.best_words.copy() + [new_word], key=len, reverse=True)
        if temp[:10] == self.best_words:
            return
        
        self.best_words = temp[:10]
        with open(self.PATH, 'w+') as file:
            for words in self.best_words:
                file.write(words + "\n")