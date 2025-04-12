from blackjack import BlackjackGame, CardDisplay
from bot import BlackjackBot

def run_bot_game():
    print("Starting a new blackjack game with the bot...\n")

    bot = BlackjackBot()
    game_result = bot.play_game(BlackjackGame)
    CardDisplay.show_game_state(game_result, show_all=True)

    print(f"\n Final Result: {game_result['winner'].upper()}")

if __name__ == "__main__":
    run_bot_game()