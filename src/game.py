from blackjack import BlackjackGame, CardDisplay

total_chips = 10
while True:
    check_exit = input("Continue? (exit)")
    
    if check_exit == "exit":
        break
    game = BlackjackGame()
    game_state = game.start_game()
    

    blackjack_result = game.check_blackjack()
    if blackjack_result:
        print("Game ended with blackjack")
        CardDisplay.show_game_state(blackjack_result)
    else:
        while True:

            CardDisplay.show_game_state(game_state)

            action = input("Do you want to hit or stand? (h/s): ").lower()
            
            if action == 'h':
                game_state = game.player_hit()
                CardDisplay.show_game_state(game_state)
                
                if 'winner' in game_state:
                    break
            elif action == 's':
                game_state = game.player_stand()
                CardDisplay.show_game_state(game_state)
                break
        
        CardDisplay.show_game_state(game_state)
        print(f"Winner: {game_state['winner']}")