import pickle
import random

class Agent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.99, exploration_rate=0.5):
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_values = {}

    def get_state(self):
        # 回傳當前狀態
        # 這個方法應該根據你的具體問題在子類別中實現
        pass

    def choose_action(self):
        state = self.get_state()

        # 探索與利用
        if random.uniform(0, 1) < self.exploration_rate:
            # 隨機選擇一個行動
            action = random.choice(self.actions)
        else:
            # 選擇具有最高Q值的行動
            q_values = [self.q_values.get((state, action), 0) for action in self.actions]
            max_q_value = max(q_values)
            count = q_values.count(max_q_value)

            # 如果有多個行動具有相同的最高Q值，則隨機選擇其中之一
            if count > 1:
                best_actions = [i for i in range(len(self.actions)) if q_values[i] == max_q_value]
                action_index = random.choice(best_actions)
            else:
                action_index = q_values.index(max_q_value)

            action = self.actions[action_index]

        return action

    def learn(self, state, action, reward, next_state):
        # 更新(state, action)對應的Q值
        old_q_value = self.q_values.get((state, action), None)
        next_state_q_values = [self.q_values.get((next_state, a), 0) for a in self.actions]
        next_state_max_q_value = max(next_state_q_values)
        new_q_value = reward + self.discount_factor * next_state_max_q_value

        if old_q_value is None:
            self.q_values[(state, action)] = new_q_value
        else:
            self.q_values[(state, action)] = old_q_value + self.learning_rate * (new_q_value - old_q_value)

    def save(self, filename):
        # 使用pickle將Q值存儲到文件中
        with open(filename, 'wb') as f:
            pickle.dump(self.q_values, f)

    def load(self, filename):
        # 使用pickle從文件中加載Q值
        with open(filename, 'rb') as f:
            self.q_values = pickle.load(f)

class MyAgent(Agent):
    def get_state(self):
        # 回傳當前狀態
        # 這個方法應該根據你的具體問題在子類別中實現
        pass

    def train(self, num_episodes=100):
        for i in range(num_episodes):
            # 重置環境並獲得初始狀態
            state = self.get_state()

            # 開始本次 episode
            while True:
                # 選擇一個行動
                action = self.choose_action()

                # 執行行動並觀察下一個狀態和獎勵
                next_state, reward = self.take_action(action)

                # 更新 (state, action) 對應的 Q-value
                self.learn(state, action, reward, next_state)

                # 移動到下一個狀態
                state = next_state

                # 檢查 episode 是否結束
                if self.is_episode_over():
                    break

    def take_action(self, action):
        # 執行指定的行動並返回下一個狀態和獎勵
        # 這個方法應該根據你的具體問題在子類別中實現
        pass

    def is_episode_over(self):
        # 檢查當前 episode 是否結束
        # 這個方法應該根據你的具體問題在子類別中實現
        pass    

#   Example usage
actions = ['left', 'right', 'up', 'down']
agent = MyAgent(actions)
agent.train()
agent.save('q_values.pkl')

# To load the saved Q-values and continue training:
agent.load('q_values.pkl')
agent.train()