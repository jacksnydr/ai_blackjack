from blackjack import BlackjackGame
from bot import BlackjackBot

#This file is pretty obvious, but it gives a User-Friendly result that allows for human evaluation
def evaluate(num_games=1000):
    bot = BlackjackBot("trained_blackjack_bot.pth")

    win, lose, push = 0, 0, 0

    for _ in range(num_games):
        result = bot.play_game(BlackjackGame)
        winner = result['winner']
        if 'player' in winner:
            win += 1
        elif winner == 'push':
            push += 1
        else:
            lose += 1

    print(f"\n Evaluation over {num_games} games:")
    print(f" Wins:  {win} ({win/num_games:.2%})")
    print(f" Losses: {lose} ({lose/num_games:.2%})")
    print(f" Pushes: {push} ({push/num_games:.2%})")

if __name__ == "__main__":
    evaluate()
