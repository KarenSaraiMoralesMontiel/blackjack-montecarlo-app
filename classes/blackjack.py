from classes.card import Card
from classes.deck import Deck
import random

class Blackjack_Game:
    def __init__(self, starting_balance=100, multiple_win= 3, bet = 10):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.starting_balance = starting_balance
        self.balance = starting_balance
        self.wins = 0
        self.loses = 0
        self.bet = bet
        self.multiple_win = multiple_win
        self.total_rounds = 0  # New variable to track total rounds played
        self.total_wins = 0    # New variable to track total wins

    def deal_initial(self):
        """Deals cards to both player and dealer
        """
        for _ in range(2):
            self.player_hand.append(self.deck.deal_card())
            self.dealer_hand.append(self.deck.deal_card())

    def calculate_score(self, hand) -> int:
        """Calculates the score of a hand

        Args:
            hand (list): A list of cards holding the hand

        Returns:
            int: Score of the hand
        """
        score = 0
        num_aces = 0
        for card in hand:
            if card.value.isdigit():
                score += int(card.value)
            elif card.value in ['Jack', 'Queen', 'King']:
                score += 10
            else:
                num_aces += 1
                score += 11
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score


    def player_turn(self):
        """Player's turn

        Returns:
            bool: Returns if the player can still play
        """
        while True:
            choice = random.choice(['h' , 's'])
            if choice == 'h':
                self.player_hand.append(self.deck.deal_card())
                player_score = self.calculate_score(self.player_hand)
                if player_score > 21:
                    self.balance -= self.bet
                    self.loses += self.bet
                    return False
            elif choice == 's':
                break
        return True

    def dealer_turn(self):
        """Dealer's play logic
        """
        dealer_score = self.calculate_score(self.dealer_hand)
        if dealer_score == 21:
            self.balance -= self.bet
            self.loses += self.bet
            return
        while dealer_score < 17:
            self.dealer_hand.append(self.deck.deal_card())
            dealer_score = self.calculate_score(self.dealer_hand)
        if dealer_score > 21 or dealer_score < self.calculate_score(self.player_hand):
            self.balance += self.bet*self.multiple_win
            self.wins += self.bet*self.multiple_win
            self.total_wins += 1  # Increment total wins
        elif dealer_score == self.calculate_score(self.player_hand):
            pass
        else:
            self.balance -= self.bet
            self.loses += self.bet

    def play(self, rounds_to_play=10):
        """A BlackJack Game

        Args:
            rounds_to_play (int, optional): Rounds to play in game. Defaults to 10.

        Returns:
            list: Data from the play
        """
        for round in range(1, rounds_to_play + 1):
            if self.balance <= 0:
                break
        self.player_hand.clear()
        self.dealer_hand.clear()
        #self.bet = 10
        self.total_rounds += 1  # Increment total rounds played
        self.deal_initial()
        if self.player_turn():
            self.dealer_turn()
        total_loses = self.total_rounds - self.total_wins
        return [self.total_wins, total_loses,  self.wins, self.loses,  self.balance, self.starting_balance]
