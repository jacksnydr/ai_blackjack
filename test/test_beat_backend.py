import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from blackjack import BlackjackGame, CardDisplay
from bot import BlackjackBot
from beat_the_bot_backend import BeatTheBotGame

total_chips = 10
while True:
    check_exit = input("Continue? (exit)")

    if check_exit == "exit":
        break

    beat_game = BeatTheBotGame("src/trained_blackjack_bot.pth")
    game_state = beat_game.start_game()

    blackjack_result = beat_game.game.check_blackjack()
    if blackjack_result:
        print("Game ended with blackjack")
        CardDisplay.show_game_state(blackjack_result, show_all=True)
    else:
        while True:
            CardDisplay.show_game_state(game_state)

            action = input("Do you want to hit or stand? (h/s): ").lower()

            if action == 'h':
                game_state = beat_game.player_hit()
                CardDisplay.show_game_state(game_state)

                if 'winner' in game_state:
                    break
            elif action == 's':
                game_state = beat_game.player_stand()
                CardDisplay.show_game_state(game_state)
                break

        print("\nBot playing...")
        game_state = beat_game.bot_play()
        CardDisplay.show_game_state(game_state)

        print("\nDealer playing...")
        game_state = beat_game.dealer_finish()
        CardDisplay.show_game_state(game_state, show_all=True)

        print(f"\nWinner: {game_state['winner']}")
