import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_layers, output_size):
        super().__init__()


        """
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size//2)
        self.linear3 = nn.Linear(hidden_size//2, output_size)
        self.to(device)
        """
        self.layers = nn.ModuleList()
        self.layers.append(nn.Linear(input_size, hidden_layers[0]))
        for i in range(1, len(hidden_layers)):
            self.layers.append(nn.Linear(hidden_layers[i - 1], hidden_layers[i]))
        self.layers.append(nn.Linear(hidden_layers[-1], output_size))
        self.to(device)

    def forward(self, x):
        """
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        #x = F.relu(self.linear3(x))
        #x = F.relu(self.linear4(x))
        #x = self.linear5(x)
        """
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
        x = self.layers[-1](x)
        return x
    
    def save(self, file_name="model.pth"):
        model_folder_path = "./models"
        os.makedirs(model_folder_path, exist_ok=True)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)



class QTrainer():
    def __init__(self, model, target_model, lr, gamma):
        self.model = model
        self.target_model = target_model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()


    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float, device=device)
        next_state = torch.tensor(next_state, dtype=torch.float, device=device)
        action = torch.tensor(action, dtype=torch.float, device=device)
        reward = torch.tensor(reward, dtype=torch.float, device=device)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: Get predcited Q values with current state
        pred = self.model(state)
        next_q = self.model(next_state)
        target = pred.clone().detach()

        with torch.no_grad():
            next_q_target = self.target_model(next_state)

        for idx in range(len(done)):
            
            if not done[idx]: # 2: Apply r + y * max(next_predicted Q values)
                Q_new = reward[idx] + self.gamma * torch.max(next_q_target[idx])
            else:
                Q_new = reward[idx]

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        
        
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        
        loss.backward()

        self.optimizer.step()

        return loss