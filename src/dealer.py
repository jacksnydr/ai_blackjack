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

    def get_full_score(self):
        temp_score = 0
        aces = 0

        for card_info in self.hand:
            card = card_info["card"]
            value = int(card.split('-')[0])

            if value == 1:
                aces += 1
                temp_score += 11
            elif value > 10:
                temp_score += 10
            else:
                temp_score += value

        while temp_score > 21 and aces > 0:
            temp_score -= 10
            aces -= 1

        return temp_score

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
        self.is_showing = True
        temp_score = 0
        aces = 0
        
        for card_info in self.hand:
            card = card_info["card"]
            value = int(card.split('-')[0])
            
            if value == 1:
                aces += 1
                temp_score += 11
            elif value > 10:
                temp_score += 10
            else:
                temp_score += value
        
        while temp_score > 21 and aces > 0:
            temp_score -= 10
            aces -= 1
        
        return temp_score
    
    def play_hand(self):
        self.is_showing = True

        while self.get_full_score() < 17:
            self.add_card(self.deck.deal())

        for card_info in self.hand:
            card_info["hidden"] = False

        self.calculate_score()

        return self.score
    
    def check_blackjack(self):
        temp_score = 0
        aces = 0

        for card_info in self.hand:
            card = card_info["card"]
            value = int(card.split('-')[0])

            if value == 1:
                aces += 1
                temp_score += 11
            elif value > 10:
                temp_score += 10
            else:
                temp_score += value

        while temp_score > 21 and aces > 0:
            temp_score -= 10
            aces -= 1

        return temp_score == 21 and len(self.hand) == 2
    
    def show_hand(self, reveal_all=False):
        cards = []
        for card_info in self.hand:
            if card_info["hidden"] and not reveal_all and not self.is_showing:
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