from blackjack import BlackjackGame, CardDisplay
from bot import BlackjackBot
#Runnable file that calls the model on a bot instance
# Simply defines bot, starts game, shows results, and prints for usability
def run_bot_game():
    bot = BlackjackBot()  # For Training Loop? - BlackjackBot("model.pth")
    while True:
        print("\n Starting a new game...\n")
        game_result = bot.play_game(BlackjackGame)

        CardDisplay.show_game_state(game_result, show_all=True)
        print(f"\n Final Result: {game_result['winner'].upper()}")

        user_input = input("\nPress Enter for the bot to play another game, or type 'q' to quit: ").strip().lower()
        if user_input == 'q':
            print("\n Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    run_bot_game()