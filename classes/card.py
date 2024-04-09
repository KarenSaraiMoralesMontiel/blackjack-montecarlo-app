"""
card.py
This file contains the Letter class.
Its parameters are the suit and the value of the card.
Author: Karen Sarai Morales Montiel
Creation date: April 1, 2024
"""

class Card:
  """Card class, simulates a card in the deck
  """
  def __init__(self, suit, value):
    self.suit = suit
    self.value = value

  def __repr__(self):
    return f"{self.value} of {self.suit}"