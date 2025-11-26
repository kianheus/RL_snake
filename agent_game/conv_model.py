import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class CNN_QNet(nn.Module):
    def __init__(self, board_size, output_size):
        super().__init__()

        self.conv_layers = nn.Sequential(
            nn.Conv2d(6, 32, kernel_size = 5, stride = 1, padding = 2),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size = 5, stride = 1, padding = 2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size = 3, stride = 1, padding = 1),
            nn.ReLU()
        )

        conv_out_size = 64 * board_size * board_size

        self.fc_layers = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, output_size)
        )

    def forward(self, x):
        if x.dim() == 3:
            x = x.unsqueeze(0)
        x = self.conv_layers(x)
        x = torch.flatten(x, 1)
        x = self.fc_layers(x)
        return x
    
    def save(self, file_name="model.pth"):
        model_folder_path = "./models"
        os.makedirs(model_folder_path, exist_ok=True)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)



class QTrainer():
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()


    def train_step(self, state, action, reward, next_state, done):

        reward = torch.tensor(reward, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)

        if state.dim() == 3:
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: Get predcited Q values with current state
        pred = self.model(state)

        target = pred.clone().detach()

        next_pred = self.model(next_state)

        for idx in range(state.shape[0]):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state))

            target[idx][torch.argmax(action).item()] = Q_new

        # 2: Apply r + y * max(next_predicted Q values)
        
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()