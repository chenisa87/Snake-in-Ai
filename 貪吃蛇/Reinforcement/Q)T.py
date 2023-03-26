import numpy as np
import pandas as pd
import random
import pygame
import math
import os

model_path = os.path.dirname(os.path.abspath(__file__)) + "/log/qtable.pickle"

class QLearningTable:
    def __init__(self,actions,learning_rate=0.05,reward_decay=0.9,e_greedy=0): # e_greedy 改成 0 執行 0.1 訓練
       
        self.actions=actions
        self.lr=learning_rate
        self.gamma=reward_decay
        self.epsilon=e_greedy

        self.q_table=pd.DataFrame(columns=self.actions,dtype=np.float64)
        #跑過一次後請註解掉此行
        #self.q_table.to_pickle(model_path)

        self.q_table =pd.read_pickle(model_path)
        
    
    def choose_action(self,observation):
        self.check_state_exist(observation)

        #action selection
        if np.random.uniform()>self.epsilon:
            state_action =self.q_table.loc[observation,:]
            action =np.random.choice(state_action[state_action==np.max(state_action)].index)
        else:
            action = np.random.choice(self.actions)
        
        return action
    
    def learn(self,s,a,r,s_):
        self.check_state_exist(s)
        self.check_state_exist(s_)
        q_predict=self.q_table.loc[s,a]
        if s_!='Game_over' or s_!='Game_pass':
            q_target =r+self.gamma*self.q_table.loc[s_,:].max()
        else:
            q_target=r
        self.q_table.loc[s,a]+=self.lr*(q_target-q_predict)
    
    def check_state_exist(self,state):
        if state not in list(self.q_table.index):
            self.q_table=self.q_table.append(pd.Series([0]*len(self.actions),index=self.q_table.columns,name=state,))


class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.frame=0
        self.status=0
        self.x = 0
        self.y = 0
        self.end_x = 0
        self.end_y = 0
        self.r_sensor_value = 0
        self.l_sensor_value = 0
        self.f_sensor_value = 0
        self.l_t_sensor_value = 0
        self.r_t_sensor_value= 0
        self.angle=0
        self.control_list = {"left_PWM" : 0, "right_PWM" : 0}
        self.observation = 0
        self.action = 0
        self.crash_times =0
        self.check_points=[]
        self.ggtime = 1
        # print("Initial ml script")
        print(kwargs)


        self.action_space = [["SPEED"],["BRAKE"],["left_PWM"],["right_PWM"]]
        self.n_actions = len(self.action_space)
        self.RL = QLearningTable(actions=list(range(self.n_actions)))

        self.status = "GAME_ALIVE"
        self.state = [self.observation]
        self.state_ = [self.observation]



    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        
        
        def check():        # 設定observation，需要加東西
            self.observation = 0
            self.frame=scene_info["frame"]
            self.status=scene_info["status"]
            self.r_sensor_value = scene_info["R_sensor"]
            self.l_sensor_value = scene_info["L_sensor"]
            self.f_sensor_value = scene_info["F_sensor"]
            self.l_t_sensor_value = scene_info["L_T_sensor"]
            self.r_t_sensor_value = scene_info["R_T_sensor"]
            self.x = scene_info["x"]
            self.y = scene_info["y"]
            self.end_x = scene_info["end_x"]
            self.end_y = scene_info["end_y"]
            self.angle = scene_info["angle"]
            self.crash_times=scene_info["crash_times"]
            self.check_points=scene_info["check_points"]

            


            if self.f_sensor_value >15:
                self.observation = 0 #衝刺
        
            elif (self.l_sensor_value + self.l_t_sensor_value*1.5) > (self.r_sensor_value + self.r_t_sensor_value*1.5):
                print("5")
                self.observation = 5
                #左大轉左

            elif  (self.r_sensor_value + self.r_t_sensor_value*1.5) > (self.l_sensor_value + self.l_t_sensor_value*1.5):
                self.observation = 6
                print("6")
            elif self.f_sensor_value < 10 and self.l_t_sensor_value < 10:
                self.observation = 1
                #轉右邊大的

            elif self.f_sensor_value < 10 and self.r_t_sensor_value < 10:
                self.observation = 2
                #轉左邊大的
            elif self.l_t_sensor_value < 12:
                self.observation = 3
                #小轉右的
            elif self.r_t_sensor_value < 12:
                self.observation = 4
                #小轉左的
            elif (self.l_sensor_value) -30> (self.r_sensor_value):
                self.observation = 9
                #左邊很大 轉左邊

            elif  (self.r_sensor_value) -30> (self.l_sensor_value):
                self.observation = 10
                #右邊很大 轉右邊 
            
                #右大轉右

            
            elif self.f_sensor_value > 15 and self.l_t_sensor_value >20:
                self.observation = 21
            elif self.f_sensor_value > 15 and self.r_t_sensor_value >20:
                self.observation = 22

            #第二關
            elif (self.l_t_sensor_value) -30> (self.r_t_sensor_value):
                self.observation = 11
                #print("左邊很大 轉左邊")

            elif  (self.r_t_sensor_value) -30> (self.l_t_sensor_value):
                self.observation = 12
                #print("右邊很大 轉右邊")
            

            elif self.r_sensor_value < 2:
                self.observation = 13
                #print("右邊快到 轉左邊")
            elif self.l_sensor_value < 2:
                self.observation = 14
                #print("左邊快到 轉右邊")

            
            
            
            elif self.l_t_sensor_value < 3 or self.r_t_sensor_value <3 or self.f_sensor_value <10:
                self.observation = 15

            if self.l_sensor_value < 1 or self.r_sensor_value <1 or self.f_sensor_value <1 or self.r_t_sensor_value < 1 or self.l_t_sensor_value <1:
                self.observation = 16
            
            if self.frame == 10:
                self.observation = 17

            if self.crash_times == self.ggtime:
                self.ggtime +=1
                self.observation = 18
            if self.frame == 1790:
                self.observation = 19

            if self.end_x - 4 <= self.x <= self.end_x + 4 and self.y -4 <= self.end_y <= self.y +4:
                self.observation = 20

            print(self.observation)

            

        
            
    
            
            
        def step(self, state):      # 設reward，需要加東西
            self.reward = 0
            action = self.action
            

            if state == [0]:
                self.reward += 50
                if action == 0:
                    self.reward += 50
                if action == 1:
                    self.reward += -200
                if action == 2:
                    self.reward += -50
                if action == 3:
                    self.reward += -50

            return self.reward



        check()
        self.state_ = [self.observation]
        self.reward = step(self,self.state_)
        action = self.RL.choose_action(str(self.state))
        self.RL.learn(str(self.state), self.action, self.reward, str(self.state_))
        self.action = action
        self.state = self.state_



        if action==0:
            self.control_list["left_PWM"] = 200
            self.control_list["right_PWM"] = 200
        elif action==1:
            self.control_list["left_PWM"] = -150
            self.control_list["right_PWM"] = -150
        elif action==2:
            self.control_list["left_PWM"] = -100
            self.control_list["right_PWM"] = 100
        else:
            self.control_list["left_PWM"] = 100
            self.control_list["right_PWM"] = -100




        return self.control_list

    def reset(self):
        """
        Reset the status
        """
        print(self.RL.q_table)
        self.RL.q_table.to_pickle(model_path)
        pass
