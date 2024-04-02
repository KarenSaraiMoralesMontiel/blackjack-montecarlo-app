import random
from classes.card import Card
class Deck:
    def __init__(self):
        self.cards = []
        self.shuffle_deck()

    def shuffle_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) == 0:
            self.shuffle_deck()
        return self.cards.pop()