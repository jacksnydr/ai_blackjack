from deck import Deck
from dealer import Dealer, Player

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer(self.deck)
        self.player = Player()
        
    def start_game(self):
        self.dealer.deal_initial_cards(self.player)
        return {
            "player_hand": self.player.hand,
            "player_score": self.player.score,
            "dealer_hand": self.dealer.show_hand(),
            "dealer_visible_score": self.dealer.score,
            "dealer_score": None
        }
    
    def player_hit(self):
        self.player.add_card(self.deck.deal())
        
        if self.player.score > 21:
            return self.end_round("dealer")
            
        return {
            "player_hand": self.player.hand,
            "player_score": self.player.score,
            "dealer_hand": self.dealer.show_hand(),
            "dealer_visible_score": self.dealer.score,
            "dealer_score": None
        }
    
    def player_stand(self):
        self.dealer.play_hand()
        return self.determine_winner()
    
    def determine_winner(self):
        if self.player.score > 21:
            winner = "dealer"
        elif self.dealer.score > 21:
            winner = "player"
        elif self.player.score > self.dealer.score:
            winner = "player"
        elif self.dealer.score > self.player.score:
            winner = "dealer"
        else:
            winner = "push"
            
        return self.end_round(winner)
    
    def end_round(self, winner):
        return {
            "player_hand": self.player.hand,
            "player_score": self.player.score,
            "dealer_hand": self.dealer.show_hand(reveal_all=True),
            "dealer_score": self.dealer.score,
            "winner": winner
        }
    
    def check_blackjack(self):
        player_blackjack = self.player.check_blackjack()
        dealer_blackjack = self.dealer.check_blackjack()
        
        if player_blackjack and dealer_blackjack:
            return self.end_round("push")
        elif player_blackjack:
            return self.end_round("player_blackjack")
        elif dealer_blackjack:
            return self.end_round("dealer_blackjack")
        
        return None
    
class CardDisplay:
    
    @staticmethod
    def print_cards(cards, hidden=None):
        if hidden is None:
            hidden = [False] * len(cards)
        
        value_map = {
            "1": "A", "11": "J", "12": "Q", "13": "K",
            "2": "2", "3": "3", "4": "4", "5": "5", 
            "6": "6", "7": "7", "8": "8", "9": "9", "10": "10"
        }
        
        suit_map = {
            "h": "♥", "d": "♦", "c": "♣", "s": "♠"
        }
        
        height = 5
        
        card_rows = [[] for _ in range(height)]
        
        for i, card in enumerate(cards):
            if hidden[i]:
                card_rows[0].append("┌─────┐")
                card_rows[1].append("│░░░░░│")
                card_rows[2].append("│░░░░░│")
                card_rows[3].append("│░░░░░│")
                card_rows[4].append("└─────┘")
            else:
                value, suit = card.split("-")
                display_value = value_map[value]
                suit_symbol = suit_map[suit]
                
                if display_value == "10":
                    value_display = "10"
                    value_spacer = ""
                else:
                    value_display = display_value
                    value_spacer = " "
                
                card_rows[0].append(f"┌─────┐")
                card_rows[1].append(f"│{value_display}{value_spacer}   │")
                card_rows[2].append(f"│  {suit_symbol}  │")
                card_rows[3].append(f"│   {value_spacer}{value_display}│")
                card_rows[4].append(f"└─────┘")
        
        for row in card_rows:
            print(" ".join(row))
    
    @staticmethod
    def show_game_state(game_state, show_all=False):
        """Display the current game state with nice-looking cards"""
        print("\nDEALER'S HAND:")
        dealer_hand = game_state['dealer_hand']
        
        hidden = []
        for card in dealer_hand:
            if card == "HIDDEN":
                hidden.append(True)
            else:
                hidden.append(False)
        
        dealer_cards = [card if card != "HIDDEN" else "1-s" for card in dealer_hand]
        CardDisplay.print_cards(dealer_cards, hidden)

        if game_state.get("dealer_score") is None:
            print(f"Dealer's visible score: {game_state['dealer_visible_score']}")
        else:
            print(f"Dealer's score: {game_state['dealer_score']}")


        print("\nYOUR HAND:")
        CardDisplay.print_cards(game_state['player_hand'])
        print(f"Your score: {game_state['player_score']}")