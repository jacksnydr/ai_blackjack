from blackjack import BlackjackGame
from bot import BlackjackBot
from dealer import Player

# Backend for the demo

class BeatTheBotGame:
    def __init__(self, bot_model_path):
        self.bot = BlackjackBot(bot_model_path)
        self.game = BlackjackGame()
        self.bot_player = Player()
        self.player_done = False
        self.bot_done = False
        self.state = None

    # Adapted from BlackjackGame.start_game but with a second bot player, essentially just starts two
    # simultaneous games with the same single dealer
    def start_game(self):
        self.player_done = False
        self.bot_done = False
        self.game = BlackjackGame()
        self.state = self.game.start_game()

        self.bot_player.hand = []
        self.bot_player.score = 0
        self.bot_player.add_card(self.game.deck.deal())
        self.bot_player.add_card(self.game.deck.deal())

        return self.state

    # Player hit action
    def player_hit(self):
        self.state = self.game.player_hit()
        if self.state['player_score'] > 21:
            self.player_done = True
        return self.state

    # Stand action, both adapted from the original game
    def player_stand(self):
        self.player_done = True
        self.state = self.game.player_stand()
        return self.state

    # Bot to play turn function
    def bot_play(self):
        if self.bot_player.score == 21:
            self.bot_done = True
            return {
                "player_hand": self.bot_player.hand,
                "player_score": self.bot_player.score,
                "dealer_hand": self.game.dealer.show_hand(),
                "dealer_visible_score": self.game.dealer.score,
                "dealer_score": None
            }

        while True:
            state = {
                "player_hand": self.bot_player.hand,
                "player_score": self.bot_player.score,
                "dealer_hand": self.game.dealer.show_hand(),
                "dealer_visible_score": self.game.dealer.score,
                "dealer_score": None
            }
            # Bot chooses action based on the game state
            action = self.bot.choose_action(state)
            if action == "hit":
                self.bot_player.add_card(self.game.deck.deal())
                if self.bot_player.score > 21:
                    break
            else:
                break

        self.bot_done = True
        return {
            "player_hand": self.bot_player.hand,
            "player_score": self.bot_player.score,
            "dealer_hand": self.game.dealer.show_hand(),
            "dealer_visible_score": self.game.dealer.score,
            "dealer_score": None
        }
    
    # Dealer finish turn logic
    def dealer_play_full(self, bot_score):
        player_busted = self.state['player_score'] > 21
        bot_busted = bot_score > 21

        # Dont do anything if both players busted
        if player_busted and bot_busted:
            return

        # Typical casino rules, dealer stands on 17 hits on anything lower
        while self.game.dealer.score < 17:
            self.game.dealer.add_card(self.game.deck.deal())



    # Finish the game and finalize the dealer's hand, then figure out the outcome
    def dealer_finish(self):
        for card_info in self.game.dealer.hand:
            card_info["hidden"] = False
        self.dealer_play_full(self.bot_player.score)
        self.state = self.game.determine_winner()
        return self.state