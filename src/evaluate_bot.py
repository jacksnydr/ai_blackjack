from blackjack import BlackjackGame
from bot import BlackjackBot
import matplotlib.pyplot as plt
import numpy as np

def evaluate(num_games=1000):
    bot = BlackjackBot("trained_blackjack_bot.pth")
    win, lose, push = 0, 0, 0
    
    # Lists to track running performance
    running_wins = []
    games_played = []
    
    for i in range(num_games):
        result = bot.play_game(BlackjackGame)
        winner = result['winner']
        if 'player' in winner:
            win += 1
        elif winner == 'push':
            push += 1
        else:
            lose += 1
            
        # Track running win rate
        running_wins.append(win / (i + 1))
        games_played.append(i + 1)

    # Print statistics
    print(f"\nEvaluation over {num_games} games:")
    print(f"Wins:  {win} ({win/num_games:.2%})")
    print(f"Losses: {lose} ({lose/num_games:.2%})")
    print(f"Pushes: {push} ({push/num_games:.2%})")

    # Create visualization
    plt.figure(figsize=(15, 5))
    
    # Pie chart of outcomes
    plt.subplot(1, 2, 1)
    labels = ['Wins', 'Losses', 'Pushes']
    sizes = [win, lose, push]
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Game Outcomes Distribution')

    # Running win rate plot
    plt.subplot(1, 2, 2)
    plt.plot(games_played, running_wins, color='#2980b9')
    plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.3)
    plt.xlabel('Games Played')
    plt.ylabel('Win Rate')
    plt.title('Running Win Rate Over Time')

    plt.tight_layout()
    plt.savefig('bot_performance.png')
    plt.show()

if __name__ == "__main__":
    evaluate()
