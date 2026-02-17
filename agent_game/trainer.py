import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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