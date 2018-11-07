import torch
import torch.nn.functional as F
import numpy as np

def hidden_init(layer):
    fan_in = layer.weight.data.size()[0]
    lim = 1. / np.sqrt(fan_in)
    return (-lim, lim)

class ActorNetwork(torch.nn.Module):
    def __init__(self, state_size, action_size, seed, device):
        super(ActorNetwork, self).__init__()
        self.state_size = state_size
        self.action_size = action_size
        torch.manual_seed(seed)
        
        hidden_size = 120
        self.fc1 = torch.nn.Linear(state_size, hidden_size)
        self.fc2 = torch.nn.Linear(hidden_size, action_size)
        self.init_weights()
        
    def init_weights(self):
        self.fc1.weight.data.uniform_(*hidden_init(self.fc1))
        self.fc2.weight.data.uniform_(-3e-3, 3e-3)
        
    def forward(self, state):
        output = F.relu(self.fc1(state))
        output = torch.tanh(self.fc2(output))
        return output
    
    
class CriticNetwork(torch.nn.Module):
    def __init__(self, state_size, action_size, seed, device):
        super(CriticNetwork, self).__init__()
        self.state_size = state_size
        self.action_size = action_size
        torch.manual_seed(seed)
        
        hidden_size_1 = 120
        hidden_size_2 = 120
        self.fc1 = torch.nn.Linear(state_size, hidden_size_1)
        self.fc2 = torch.nn.Linear(hidden_size_1+action_size, hidden_size_2)
        self.fc3 = torch.nn.Linear(hidden_size_2, 1)
        self.init_weights()
        
    def init_weights(self):
        self.fc1.weight.data.uniform_(*hidden_init(self.fc1))
        self.fc2.weight.data.uniform_(*hidden_init(self.fc2))
        self.fc3.weight.data.uniform_(-3e-3, 3e-3)
        
    def forward(self, state, action):
        output = F.relu(self.fc1(state))
        output = torch.cat((output, action), dim=1)
        output = F.relu(self.fc2(output))
        output = self.fc3(output)
        return output
                        