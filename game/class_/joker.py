from bs4 import BeautifulSoup
from urllib.request import urlopen
import random


class Joker:
    def __init__(self):
        parser = BeautifulSoup(
            urlopen('https://michael78912.github.io/puns.html'), 'lxml')
        self.division = parser.p.get_text().split('\n')[2:-1]
        self.joke = random.choice(self.division).strip()

    def say_joke(self):
        print(self.joke)

    def new_joke(self):
        self.joke = random.choice(self.division)


print(Joker().joke)
