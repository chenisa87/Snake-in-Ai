import pygame
import random
from const import WIDTH,HEIGHT,BLOCK_SIZE,SPEED,BLACK,BLUE1,BLUE2,BLUEHEAD,RED,RED2,RED3,WHITE,LIGHTPINK,GRAY,YELLOW,GREEN1,GREEN2,PURPLE1,PURPLE2 
import numpy as np

"""初始化""" 

pygame.init()

"""基礎設定"""

BOOMIMAGE = pygame.transform.scale(pygame.image.load("image\\boomimage.jpg"), (20,20))
GOLDEN = pygame.transform.scale(pygame.image.load("image\\Golden.jpg"), (20,20))
APPLE = pygame.transform.scale(pygame.image.load("image\\APPLE.png"), (20,20))

font = pygame.font.Font("font.ttf",18)

"""動作"""

from enum import Enum
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

"""遊戲主程式"""

class GameAI():
    def __init__(self,width=WIDTH,height=HEIGHT):

        """基礎設定"""

        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("貪吃蛇遊戲")
        self.frame_times = 100
        self.reset()

    def reset(self):
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        """蛇的基礎樣子"""

        self.direction = random.choice([Direction.RIGHT,Direction.LEFT,Direction.UP,Direction.DOWN])
        self.head = [self.width//2,self.height//2]
        self.snake = [self.head,[self.width//2-BLOCK_SIZE,self.height//2],[self.width//2-BLOCK_SIZE*2,self.height//2]]

        """基礎素質"""

        self.health = 1
        self.score = 0
        self.grade = 0
        self.record = 0
        

        """基礎道具"""

        #初始設定

        self.bomb = None
        self.kbomb = None
        self.golden = None
        self.food = []
        self.invincibletime = 0
        self.isinvincible = False
        self.eatfoodtime = 50

        #之後的設定

        self.place_food()
        self.appleboom = []
        self.appleboomcount = 0

        self.bomblist = [20,40,60,80,100,120]
        self.goldenlist = [5,30,60,90,120]

        """計時器"""

        self.time_elapsed = 0

        """豐年祭"""

        self.time_list = [15,20,35,40,55,60,75,80,95,100,115,120]
        self.Harvest = False

        """"""

        self.frame_iteration = 0 #遊玩次數

    """主程式"""

    def main(self,action): #新增動作
        """基礎"""
        self.frame_iteration += 1
        
        

        """收集輸出"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() #關閉所有

        """移動"""

        self.move(action)

        

        """事件判斷"""
        reward = 0
        game_over = False
        self.eventexecution()
        

        if self.event() or self.frame_iteration >= 200+(100 if self.score <= 10 else 200)*len(self.snake):
            reward = -5000
            game_over = True
            return reward,game_over,self.score

        if self.head in self.food:
            print(">>>吃到食物")
            reward = 1000
        
        if self.eatfoodtime == 0:
            print(">>>肚子餓")
            reward = -200
            self.eatfoodtime = 50
        else:
            self.eatfoodtime -=1


        """if self.score == self.grade:
            if self.grade <= 6:
                self.grade += 1
            reward = -60 + self.grade * 10"""

        if self.score == self.record:
            self.record += 1
            reward = 2000
        
        self.eventspecial()

        

        return reward,game_over , self.score
    
    """更新時間"""

    def update_time(self):
        time_passed = pygame.time.get_ticks() - self.start_time
        self.time_elapsed = time_passed // 1000

    """處理事件"""
    def eventspecial(self):
    #            #炸彈放置
#
    #    if self.time_elapsed in self.bomblist:
    #        del self.bomblist[0]
#
        #    self.place_bomb()
        #    self.place_kbomb()
#
        ##豐年祭
#
        #if self.time_elapsed in self.time_list:
        #    if self.Harvest:
        #        self.HarvestFestival(False)
        #        del self.time_list[0]
        #        self.Harvest = False
        #    else:
        #        self.Harvest = True
        #        del self.time_list[0]
        #        self.HarvestFestival(True)
#
        ##無敵聖杯
#
        #if self.time_elapsed in self.goldenlist:
        #    del self.goldenlist[0]
#
        #    self.place_golden()

        """更新"""

        self.draw()
        self.clock.tick(SPEED)

        """更新時間"""

        self.update_time()

        """回傳 血量 和 分數"""
    def event(self,pt=None):
        if pt is None:
            pt = self.head
        """判斷是否撞牆壁"""
        if pt[0] < 0 or pt[0] > self.width - BLOCK_SIZE or pt[1] < 0 or pt[1] > self.height - BLOCK_SIZE:
            return True
        """判斷是否撞到自己身體"""
        if pt in self.snake[1::]:
            return True
        """判斷是否撞到炸彈 或者 拆炸彈"""
        if pt == self.bomb:
            return True
        if self.health <= 0:
            print(">>>死亡")
            return True
        return False
    """
    def eventreward(self):
        pt = self.head


        #判斷是否撞牆壁
        
        if self.isinvincible == False:
            if pt[0] < 0 or pt[0] > self.width - BLOCK_SIZE or pt[1] < 0 or pt[1] > self.height - BLOCK_SIZE:
                print(">>>撞牆")
                return -10


            #判斷是否撞到自己身體

            if pt in self.snake[1::]:
                print(">>>撞到自己")
                return -10

            #判斷是否撞到炸彈 或者 拆炸彈

            if pt == self.bomb:
                    
                print(">>>碰到炸彈")
                return -10

        else:
            self.invincibletime -= 1 
            if self.invincibletime == 0:
                self.isinvincible = False

        #炸彈判斷

        if pt == self.kbomb:
            print(">>>碰到拆彈")
            return 10

        #聖杯判斷

        if pt == self.golden:
            print(">>>碰到黃金聖杯")
            return 10

        #判斷是否長身體

        
            return -10
        else:
            self.eatfoodtime -= 1
        
        
        return 0
        """

    def eventexecution(self,pt=None):
        if pt is None:
            pt = self.head


        """判斷是否撞牆壁"""
        
        if pt[0] < 0 or pt[0] > self.width - BLOCK_SIZE or pt[1] < 0 or pt[1] > self.height - BLOCK_SIZE:
            self.health -= 1
        """判斷是否撞到自己身體"""
        if pt in self.snake[1::]:
            self.health -= 1
        """判斷是否撞到炸彈 或者 拆炸彈"""
        if pt == self.bomb:
            self.health -= 1
        
        """
        #炸彈判斷

        if pt == self.kbomb:
            self.kbomb = None
            self.bomb = None

        #聖杯判斷

        if pt == self.golden:
            #self.invincibletime = SPEED * 3
            #self.isinvincible = True
            self.golden = None
        """
        """判斷是否長身體"""

        if pt in self.food:
            self.score += 1
            self.eatfoodtime = 50
            self.appleboom = pt
            self.appleboomcount = 5
            self.food.remove(self.appleboom)
            self.place_food()

        else:
            self.snake.pop(-1)



    """放置食物"""

    def place_food(self):
        
        x = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food.append([x,y])
        """判斷是否在正確的位置"""
        if self.food in self.snake:
            self.food.pop(-1)
            self.place_food()

    """炸彈"""

    def place_bomb(self):
        x = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.bomb = [x,y]
        """判斷是否在正確的位置""" 
        if self.bomb in self.snake or self.bomb in self.food:
            self.place_bomb()

    def place_kbomb(self):
        x = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.kbomb = [x,y]
        """判斷是否在正確的位置"""
        if self.kbomb in self.snake or self.kbomb in self.food or self.kbomb == self.bomb:
            self.place_kbomb()

    """無敵聖杯"""

    def place_golden(self):
        x = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.golden = [x,y]
        """判斷是否在正確的位置""" 
        if self.golden in self.snake or self.golden in self.food:
            self.place_bomb()

    """豐年祭"""

    def HarvestFestival(self,check):
        if check:
            self.place_food()
            self.place_food()
            self.place_food()
            self.place_food()
            self.place_food()
        else:
            while len(self.food)>1:
                self.food.pop(-1)            

    """蛇的移動"""

    def move(self,action):
        """
        Action
        [1,0,0] 直
        [0,1,0] 右轉
        [0,0,1] 左轉
        """
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP] #利用順時針的方向來將四個方位定位
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]
        if np.array_equal(action,[0,1,0]):
            next_dir = (idx+1) % 4
            new_dir = clock_wise[next_dir]
        if np.array_equal(action,[0,0,1]):
            next_dir = (idx-1) % 4
            new_dir = clock_wise[next_dir]

        self.direction = new_dir
    
        x = self.head[0]
        y = self.head[1]

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        
        self.head = [x,y]
        self.snake.insert(0,self.head)

    """畫出圖"""

    def draw(self):

        self.display.fill(BLACK)

        """畫出蛇"""
        check = 0
        for snake in self.snake:
            check += 1
            if check %2==0:
                pygame.draw.rect(self.display,GREEN2,pygame.Rect(snake[0],snake[1],BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(self.display,GREEN1,pygame.Rect(snake[0]+4,snake[1]+4,BLOCK_SIZE-8,BLOCK_SIZE-8))
            else:
                pygame.draw.rect(self.display,PURPLE1,pygame.Rect(snake[0],snake[1],BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(self.display,PURPLE2,pygame.Rect(snake[0]+4,snake[1]+4,BLOCK_SIZE-8,BLOCK_SIZE-8))
            if snake == self.head:
                pygame.draw.rect(self.display,WHITE,pygame.Rect(snake[0]+0,snake[1]+4,6,6))
                pygame.draw.rect(self.display,WHITE,pygame.Rect(snake[0]+14,snake[1]+4,6,6))
                pygame.draw.rect(self.display,BLACK,pygame.Rect(snake[0]+2,snake[1]+6,3,3))
                pygame.draw.rect(self.display,BLACK,pygame.Rect(snake[0]+16,snake[1]+6,3,3))
                if self.direction == Direction.RIGHT:
                    pygame.draw.rect(self.display,RED,pygame.Rect(snake[0]+7,snake[1]+10,20,6))
                elif self.direction == Direction.LEFT:
                    pygame.draw.rect(self.display,RED,pygame.Rect(snake[0]+7-20,snake[1]+10,20,6))
                elif self.direction == Direction.UP:
                    pygame.draw.rect(self.display,RED,pygame.Rect(snake[0]+7,snake[1]-10,6,20))
                elif self.direction == Direction.DOWN:
                    pygame.draw.rect(self.display,RED,pygame.Rect(snake[0]+7,snake[1]+10,6,20))
                

        """畫出食物"""
        
        if self.appleboom != [] and self.appleboomcount >= 1:
           self.appleboomcount -= 1
           self.display.blit(BOOMIMAGE,self.appleboom)

        for food in self.food:

            self.display.blit(APPLE,[food[0],food[1]])
            #pygame.draw.rect(self.display,RED3,pygame.Rect(food[0],food[1],BLOCK_SIZE,BLOCK_SIZE))
            #pygame.draw.rect(self.display,RED2,pygame.Rect(food[0]+4,food[1]+4,BLOCK_SIZE-8,BLOCK_SIZE-8))
        
        """畫出炸彈"""
        
        if self.bomb != None:
            pygame.draw.rect(self.display,GRAY,pygame.Rect(self.bomb[0],self.bomb[1],BLOCK_SIZE,BLOCK_SIZE))
        if self.kbomb != None:
            pygame.draw.rect(self.display,YELLOW,pygame.Rect(self.kbomb[0],self.kbomb[1],BLOCK_SIZE,BLOCK_SIZE))
        
        """畫出聖杯"""

        if self.golden != None:
            self.display.blit(GOLDEN,self.golden)
        
        """畫出 分數 時間 生命值 特殊事件"""

        time_text = f"Time passed: {self.time_elapsed} s"
        time_surface = font.render(time_text, True, LIGHTPINK)
        self.display.blit(time_surface, (10, 10))

        time_text = f"Frame_iteration: {self.frame_iteration} s"
        time_surface = font.render(time_text, True, LIGHTPINK)
        self.display.blit(time_surface, (10, 43))

        time_text = f"Scores: {self.score} "
        time_surface = font.render(time_text, True, LIGHTPINK)
        self.display.blit(time_surface, (450, 10))

        time_text = f"Health: {self.health} "
        time_surface = font.render(time_text, True, LIGHTPINK)
        self.display.blit(time_surface, (450, 43))

        time_text = f"Invincibility: {self.invincibletime/10} "
        time_surface = font.render(time_text, True, LIGHTPINK)
        self.display.blit(time_surface, (450, 76))

        har = "豐年祭"
        no = "平常日"
        bomb = "炸彈出現"
        bno = ""
        time_text = f"Event: {har if self.Harvest else no} {bomb if self.bomb != None else bno} "
        time_surface = font.render(time_text, True, LIGHTPINK)
        self.display.blit(time_surface, (10,76))

        """更新視窗內容"""
        
        pygame.display.flip()
