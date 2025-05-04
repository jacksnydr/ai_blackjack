import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import random
from model import BlackjackPolicyNet
from blackjack import BlackjackGame

# gamma is the weight of future outcome value. 0.99 means that the model cares about future outcomes,
# but not more than immediate - i.e., dealer's second card
#learning rate can be changed, I have always done around 0.001 though
# epochs, number of games played in training
gamma = 0.5
learning_rate = 1e-4
epochs = 50000

# import our model
# Adam is the gradient descent optimizer, usually my go to, can try others
#loss function is mean squared error - again, can be changed but this is the only one I have used. Probably no need to test others.
model = BlackjackPolicyNet()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
loss_fn = nn.MSELoss()

# maps neural network output to action - model chooses 0 - hit, 1 - stand
action_map = ['hit', 'stand']

# build tensor for model input through current game state, same as in bot.py
def get_state_tensor(game_state):
    player_score = game_state['player_score']
    dealer_score = game_state['dealer_visible_score']
    usable_ace = any(card.startswith('1-') for card in game_state['player_hand'])
    return torch.tensor([player_score, dealer_score, int(usable_ace)], dtype=torch.float32)

# reinforcement learning method, allows the model to adjust based on importance of result
#winning is 1, push is 0 - this could be given as 0.5 maybe?, -2 if it busts, to avoid bad hits, -1 standing loss
def get_reward(winner, player_score):
    if winner == 'player' or winner == 'player_blackjack':
        return 1.0
    elif winner == 'push':
        return 0.0
    elif player_score > 21:
        return -2.0
    else:
        return -1.0

def train():
    #similar to .eval in bot.py, allows the model to change its weights/biases
    model.train()
    #keep track of loss steps every 1000 epochs for plotting
    losses = []
    epoch_steps = []
    batch_loss_sum = 0.0
    batch_loss_count = 0
    #for keeping track of training.
    win, loss, push = 0, 0, 0
    total_hits = 0
    total_stands = 0
    #currently running through 50,000 games, takes a couple of minutes but results are good.
    for epoch in range(1, epochs + 1):
        game = BlackjackGame()
        state_dict = game.start_game()
        #There is nothing to learn from a blackjack...
        if game.check_blackjack() is not None:
            continue

        transitions = []

        # starts with higher value, lowers later on to take less risky options. I.E. less strict play early in the loop
        epsilon = max(0.2, 1.0 - epoch / 10000)

        while True:
            # get state, and get qvalues through current model parameters
            state_tensor = get_state_tensor(state_dict)
            q_values = model(state_tensor)

            # epsilon greedy to randomly try new value or use the normal best value - this prevents overfitting
            #if the random action is good, weights are adjusted and it is accounted for, same if bad.
            if random.random() < epsilon:
                action_idx = random.randint(0, 1)
            else:
                action_idx = torch.argmax(q_values).item()
            #calls our action map to make a decision
            action = action_map[action_idx]
            # obviously playing game based on previous decisions
            if action == 'hit':
                next_state = game.player_hit()
                total_hits += 1
            else:
                next_state = game.player_stand()
                total_stands += 1

            done = 'winner' in next_state
            #Once game is finished, the result is grabbed, and the reward is calculated
            if done:
                reward = get_reward(next_state['winner'], next_state['player_score'])
            else:
                reward = -0.05 if action == 'hit' else 0.0
            #adds data to transitions for reference
            transitions.append((state_tensor, action_idx, reward, None if done else next_state))
            state_dict = next_state

            #For user reference, wins, pushes, losses
            if done:
                result = next_state['winner']
                if 'player' in result:
                    win += 1
                elif result == 'push':
                    push += 1
                else:
                    loss += 1
                break

        # Q-value updates, tests the progression and result of game against current model qvalue calculation and adjusts
        # if we used our q value then this shouldn't do much, but if we used the random choice, it could make a large difference, but leads to a more informed network
        for state_tensor, action_idx, reward, next_state_dict in transitions:
            q_values = model(state_tensor)

            # Compute target Q-value
            with torch.no_grad():
                if next_state_dict is not None:
                    next_state_tensor = get_state_tensor(next_state_dict)
                    next_q_values = model(next_state_tensor)
                    max_next_q = torch.max(next_q_values).item()
                    target_q = reward + gamma * max_next_q
                else:
                    target_q = reward

            # Computes mean squared error in reference to the target value and our in-game ones.
            # updates q value of chosen action
            loss = loss_fn(q_values[action_idx], torch.tensor(target_q))
            batch_loss_sum += loss.item()
            batch_loss_count += 1
            #back propogates and updates weights
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Provides information per 1000 games
        if epoch % 1000 == 0:
            total = win + loss + push
            print(f"Epoch {epoch} | Win: {win} ({win/total:.1%}), "
                  f"Loss: {loss} ({loss/total:.1%}), Push: {push} ({push/total:.1%}) | "
                  f"Hit/Stand: {total_hits}/{total_stands} | Epsilon: {epsilon:.2f}")
            # resets the user values for next 1000 epochs
            if batch_loss_count > 0:
                avg_loss = batch_loss_sum / batch_loss_count
                losses.append(avg_loss)
                epoch_steps.append(epoch)
                batch_loss_sum = 0.0
                batch_loss_count = 0
            win = loss = push = total_hits = total_stands = 0
    #Saves model in specified file to be used later
    #When changing neural network, please use a different file - I like this model currently
    torch.save(model.state_dict(), "learning_rate_lower_trained_blackjack_bot.pth")
    print("Training Loop complete. Model saved to 'trained_blackjack_bot.pth'")
    plt.figure(figsize=(10, 6))
    plt.plot(epoch_steps, losses, marker='o')
    plt.title("Average Loss by 1000 Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("Average Loss")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    train()
