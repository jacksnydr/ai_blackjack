
import torch
import torch.nn as nn

class BlackjackPolicyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 128),  # Inputs: player score, dealer visible score, usable ace (0/1)
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2)    # Outputs: [Q(hit), Q(stand)]
        )

    def forward(self, x):
        return self.net(x)
