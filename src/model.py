
import torch
import torch.nn as nn

class BlackjackPolicyNet(nn.Module):
    #Required initialization and superclass call for pytorch
    #Model takes a vector of 3 inputs (player cards, dealer cards showing, usable ace?)
    #Linear is a common layer conversion function, looks something like this: output = xW + b
    # x is the input vector, W is an arbitrarily defined weight vector, and b is an arbitrarily defined bias vector (all defined in pytorch - to be trained later)
    #RELU cleans up negative values
    #the middle layer is not necessary, but a starting point for our model structure
    #RELU cleans up negatives again
    #final Linear function provides two outputs: Q-values.
    #These Q values have no foundation thus far, but the goal will be to use reinforcement training
    # to update the arbitrary weights and biases in the model so that these Q values will lead to good choices
    #Later- the bot chooses the greatest Q-value (hit or stand) to make its decision. Meaning good Q-value calculation will be the goal of training.
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )
    #Defines sequence of hidden layers to go in the order shown above^
    def forward(self, x):
        return self.net(x)
