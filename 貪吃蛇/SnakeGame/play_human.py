import pygame
from random import randint
"""初始化"""

pygame.init()

"""基礎設定"""

WIDTH = 600
HEIGHT = 600

BLOCK_SIZE = 20
SPEED = 10

BLACK = (0,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,0,180)
BLUEHEAD = (0,0,128)
RED2 = (238,0,0)
RED3 = (150,0,0)
WHITE = (248,248,255)
RED = (255,0,0)
LIGHTPINK = (255,182,193)
GRAY = (47,79,79)
YELLOW = (255,255,0)

GREEN1 = (127,255,0)
GREEN2 = (0,205,0)

PURPLE1 = (148,0,211)
PURPLE2 = (138,43,226)

BOOMIMAGE = pygame.transform.scale(pygame.image.load("SnakeGame\\image\\boomimage.png"), (20,20))
GOLDEN = pygame.transform.scale(pygame.image.load("SnakeGame\\image\\Golden.png"), (20,20))
APPLE = pygame.transform.scale(pygame.image.load("SnakeGame\\image\\APPLE.png"), (20,20))
START = pygame.transform.scale(pygame.image.load("SnakeGame\\image\\Start.png"),(400,200))

font = pygame.font.Font("SnakeGame\\font.ttf",18)

"""動作"""

from enum import Enum
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

"""遊戲主程式"""

class Game():
    def __init__(self,width=WIDTH,height=HEIGHT):

        """基礎設定"""

        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("貪吃蛇遊戲")
        
        self.reset()

    def reset(self):
        
        self.display.fill(BLACK)
        self.display.blit(START,[100,200])
        pygame.display.flip()
        checkmouse = True
        while checkmouse:
            x1, y1 = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 100<=x1<=500 and 200<=y1<=400:
                        checkmouse = False
            
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        
        """蛇的基礎樣子"""

        self.direction = Direction.RIGHT
        self.head = [self.width//2,self.height//2]
        self.snake = [self.head,[self.width//2-BLOCK_SIZE,self.height//2],[self.width//2-BLOCK_SIZE*2,self.height//2]]

        """基礎素質"""

        self.health = 3
        self.score = 0

        """基礎道具"""

        #初始設定

        self.bomb = None
        self.kbomb = None
        self.golden = None
        self.food = []
        self.invincibletime = 0
        self.isinvincible = False

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

    """主程式"""

    def main(self):
        
        """收集輸出"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() #關閉所有
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print(">>>向左移動")
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    print(">>>向右移動")
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    print(">>>向上移動")
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    print(">>>向下移動")
                    self.direction = Direction.DOWN

        """移動"""

        self.move()

        """事件判斷"""
       
        self.eventexecution()

        #炸彈放置

        if self.time_elapsed in self.bomblist:
            del self.bomblist[0]

            self.place_bomb()
            self.place_kbomb()

        #豐年祭

        if self.time_elapsed in self.time_list:
            if self.Harvest:
                self.HarvestFestival(False)
                del self.time_list[0]
                self.Harvest = False
            else:
                self.Harvest = True
                del self.time_list[0]
                self.HarvestFestival(True)

        #無敵聖杯

        if self.time_elapsed in self.goldenlist:
            del self.goldenlist[0]

            self.place_golden()

        """更新"""

        self.draw()
        self.clock.tick(SPEED)

        """更新時間"""

        self.update_time()

        """回傳 血量 和 分數"""

        return self.health , self.score
    
    """更新時間"""

    def update_time(self):
        time_passed = pygame.time.get_ticks() - self.start_time
        self.time_elapsed = time_passed // 1000

    """處理事件"""

    def eventexecution(self):

        """判斷是否撞牆壁"""
        
        if self.isinvincible == False:
            if self.head[0] < 0 or self.head[0] > self.width - BLOCK_SIZE or self.head[1] < 0 or self.head[1] > self.height - BLOCK_SIZE:
                self.health -= 1
                self.isinvincible = True
                self.invincibletime = SPEED * 3

            """判斷是否撞到自己身體"""

            if self.head in self.snake[1::]:
                self.health -= 1
                self.isinvincible = True
                self.invincibletime = SPEED * 3

            """判斷是否撞到炸彈 或者 拆炸彈"""

            if self.head == self.bomb:
                self.health -= 1

        else:
            self.invincibletime -= 1 
            if self.invincibletime == 0:
                self.isinvincible = False

        #炸彈判斷

        if self.head == self.kbomb:
            self.kbomb = None
            self.bomb = None

        #聖杯判斷

        if self.head == self.golden:
            self.invincibletime = SPEED * 3
            self.isinvincible = True
            self.golden = None

        """判斷是否長身體"""

        if self.head in self.food:
            self.score += 1
            self.appleboom = self.head
            self.appleboomcount = 5
            self.food.remove(self.appleboom)
            self.place_food()
        else:
            self.snake.pop(-1)


    """放置食物"""

    def place_food(self):
        
        x = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food.append([x,y])
        """判斷是否在正確的位置"""
        if self.food in self.snake:
            self.food.pop(-1)
            self.place_food()

    """炸彈"""

    def place_bomb(self):
        x = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.bomb = [x,y]
        """判斷是否在正確的位置""" 
        if self.bomb in self.snake or self.bomb in self.food:
            self.place_bomb()

    def place_kbomb(self):
        x = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.kbomb = [x,y]
        """判斷是否在正確的位置"""
        if self.kbomb in self.snake or self.kbomb in self.food or self.kbomb == self.bomb:
            self.place_kbomb()

    """無敵聖杯"""

    def place_golden(self):
        x = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
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

    def move(self):
    
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
                pygame.draw.rect(self.display,PURPLE2,pygame.Rect(snake[0],snake[1],BLOCK_SIZE,BLOCK_SIZE))
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
        self.display.blit(time_surface, (10,43))

        """更新視窗內容"""
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    while True:
        health , score = game.main()
        
        if health == 0:
            game.reset()