from blackjack import BlackjackGame
from bot import BlackjackBot
from dealer import Player

class BeatTheBotGame:
    def __init__(self, bot_model_path):
        self.bot = BlackjackBot(bot_model_path)
        self.game = BlackjackGame()
        self.bot_player = Player()
        self.player_done = False
        self.bot_done = False
        self.state = None

    def start_game(self):
        self.player_done = False
        self.bot_done = False
        self.state = self.game.start_game()

        self.bot_player.hand = []
        self.bot_player.score = 0
        self.bot_player.add_card(self.game.deck.deal())
        self.bot_player.add_card(self.game.deck.deal())

        return self.state

    def player_hit(self):
        self.state = self.game.player_hit()
        if self.state['player_score'] > 21:
            self.player_done = True
        return self.state

    def player_stand(self):
        self.player_done = True
        self.state = self.game.player_stand()
        return self.state

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
    
    def dealer_play_full(self, bot_score):
        player_busted = self.state['player_score'] > 21
        bot_busted = bot_score > 21

        if player_busted and bot_busted:
            return

        while self.game.dealer.score < 17:
            self.game.dealer.add_card(self.game.deck.deal())



    def dealer_finish(self):
        self.dealer_play_full(self.bot_player.score)
        self.state = self.game.determine_winner()
        return self.state
