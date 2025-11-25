import pygame
import numpy as np
import time
from typing import List

colorGreen = (173, 204, 96)
colorDarkGreen = (43, 51, 24)

cell_size = 30
cell_count = 20
window_size = cell_size * cell_count


pygame.init()

screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Snake Game")


lastUpdateTime = time.time()



def elementInList(element: np.ndarray, list: List[np.ndarray]) -> bool:

    for item in list:
        if np.array_equal(element, item):
            return True

    return False

def eventTriggered(interval: float) -> bool:
    global lastUpdateTime

    currentTime = time.time()

    
    if (currentTime - lastUpdateTime) >= interval:

        lastUpdateTime = currentTime
        return True
    else:
        return False


class Square():
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill(colorDarkGreen)

class Snake():

    def __init__(self):
        self.addSegment = False
        self.Reset()

    
    def Draw(self):
        for item in self.body:
            x = item[0]
            y = item[1]
            square = Square()
            screen.blit(square.surf, (x * cell_size, y * cell_size))
    

    def Update(self):

        self.body.insert(0, self.body[0] + self.direction)

        if self.addSegment:
            self.addSegment = False
        else:
            self.body.pop()

    def Reset(self):
        self.body = [np.array([3,3]), np.array([2,3]), np.array([1,3])]
        self.direction = NONE


class Food():

    def __init__(self, snakeBody: List[np.ndarray]):
        self.image = pygame.image.load("graphics/food.png")
        self.image.convert_alpha()
        pygame.transform.scale(self.image, (cell_size, cell_size))
        self.position = self.GenerateRandomPos(snakeBody)


    def Draw(self):

        screen.blit(self.image, (self.position*cell_size, self.position*cell_size))

    def GenerateRandomCell(self) -> np.ndarray:
        return np.random.randint(0, cell_count, size=2)
    
    def GenerateRandomPos(self, snakeBody: List[np.ndarray]) -> np.ndarray:

        position = self.GenerateRandomCell()

        while elementInList(position, snakeBody):
            position = self.GenerateRandomCell()
        
        return position


class Game():

    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.running = False

    def Draw(self):
        self.food.Draw()
        self.snake.Draw()
    
    def Update(self):

        if self.running:
            self.snake.Update()
            self.CheckCollisionWithFood()
            self.CheckCollisionWithEdges()
            self.CheckCollisionWithTail()

    def CheckCollisionWithFood(self):

        if np.array_equal(self.snake.body[0], self.food.position):
            self.food.position = self.food.GenerateRandomPos(self.snake.body)
            self.snake.addSegment = True

    def CheckCollisionWithEdges(self):

        if self.snake.body[0][0] == -1 or self.snake.body[0][0] == cell_count or self.snake.body[0][1] == -1 or self.snake.body[0][1] == cell_count:
            self.GameOver()

    def CheckCollisionWithTail(self):

        headlessBody = self.snake.body[1::]
        if(elementInList(self.snake.body[0], headlessBody)):
            self.GameOver()

    def GameOver(self):

        self.snake.Reset()
        self.food.position = self.food.GenerateRandomPos(self.snake.body)
        self.running = False

game = Game()




if __name__ == "__main__":
        
    game = Game()


    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2
    action = STRAIGHT

    screen.fill(colorGreen)
    game.snake.Draw()
    game.food.Draw()

    pygame.display.flip()
                

    WindowShouldClose = False
    while not WindowShouldClose:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                WindowShouldClose = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    WindowShouldClose = True

                if event.key == pygame.K_UP:
                    action = STRAIGHT
                if event.key == pygame.K_RIGHT:
                    action = RIGHT
                if event.key == pygame.K_LEFT:
                    action = LEFT

                game.Step(action)

                screen.fill(colorGreen)
                game.snake.Draw()
                game.food.Draw()

            pygame.display.flip()
    pygame.quit()