import torch
from model import BlackjackPolicyNet

class BlackjackBot:
    def __init__(self, model_path=None):
        self.model = BlackjackPolicyNet()
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def get_state_tensor(self, game_state):
        player_score = game_state['player_score']
        dealer_score = game_state['dealer_visible_score']
        usable_ace = any(card.startswith('1-') for card in game_state['player_hand'])
        return torch.tensor([[player_score, dealer_score, int(usable_ace)]], dtype=torch.float32)

    def choose_action(self, game_state):
        state_tensor = self.get_state_tensor(game_state)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        action = torch.argmax(q_values).item()
        return 'hit' if action == 0 else 'stand'

    def play_game(self, game_class):
        game = game_class()
        state = game.start_game()

        bj_result = game.check_blackjack()
        if bj_result is not None:
            return bj_result

        while True:
            action = self.choose_action(state)
            print(f"Bot chose {action.upper()}")
            if action == 'hit':
                state = game.player_hit()
                if state.get("winner"):
                    return state
            else:
                return game.player_stand()
