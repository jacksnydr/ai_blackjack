import random
from deck import Deck

class Dealer:
    def __init__(self, deck=None):
        self.deck = deck if deck else Deck()
        self.hand = []
        self.score = 0
        self.is_showing = False

    def deal_initial_cards(self, player):
        player.hand = []
        player.score = 0
        self.hand = []
        self.score = 0
        
        player.add_card(self.deck.deal())
        self.add_card(self.deck.deal())
        player.add_card(self.deck.deal())
        self.add_card(self.deck.deal(), is_hidden=True)

    def add_card(self, card, is_hidden=False):
        self.hand.append({"card": card, "hidden": is_hidden})
        if not is_hidden:
            self.calculate_score()

    def calculate_score(self):
        self.score = 0
        aces = 0
        
        for card_info in self.hand:
            if card_info["hidden"]:
                continue
                
            card = card_info["card"]
            value = int(card.split('-')[0])
            
            if value == 1:
                aces += 1
                self.score += 11
            elif value > 10:
                self.score += 10
            else:
                self.score += value
        
        while self.score > 21 and aces > 0:
            self.score -= 10
            aces -= 1
    
    def reveal_hand(self):
        for card_info in self.hand:
            card_info["hidden"] = False
        self.is_showing = True
        self.calculate_score()
        return self.score
    
    def play_hand(self):
        self.reveal_hand()
        
        while self.score < 17:
            self.add_card(self.deck.deal())
        
        return self.score
    
    def check_blackjack(self):
        self.reveal_hand()
        
        return self.score == 21 and len(self.hand) == 2
    
    def show_hand(self, reveal_all=False):
        if reveal_all:
            self.reveal_hand()
            
        cards = []
        for card_info in self.hand:
            if card_info["hidden"]:
                cards.append("HIDDEN")
            else:
                cards.append(card_info["card"])
                
        return cards

class Player:
    def __init__(self):
        self.hand = []
        self.score = 0
        
    def add_card(self, card):
        self.hand.append(card)
        self.calculate_score()
        
    def calculate_score(self):
        self.score = 0
        aces = 0
        
        for card in self.hand:
            value = int(card.split('-')[0])
            
            if value == 1:
                aces += 1
                self.score += 11
            elif value > 10:
                self.score += 10
            else:
                self.score += value
        
        while self.score > 21 and aces > 0:
            self.score -= 10
            aces -= 1
    
    def check_blackjack(self):
        return self.score == 21 and len(self.hand) == 2