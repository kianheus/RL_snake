import pygame
import numpy as np
import time
from typing import List
from agent_game.connectivity_checker import check_reachable

colorGreen = (173, 204, 96)
colorDarkGreen = (43, 51, 24)

cell_size = 30
cell_count = 20
window_size = cell_size * cell_count

LEFT = [1, 0, 0]
STRAIGHT = [0, 1, 0]
RIGHT = [0, 0, 1]

NORTH = np.array([0, -1])
EAST = np.array([1, 0])
SOUTH = np.array([0, 1])
WEST = np.array([-1, 0])

DIRECTIONS = [
    NORTH,
    EAST,
    SOUTH,
    WEST
]

pygame.init()

screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Snake Game")


lastUpdateTime = time.time()



def elementInList(element: np.ndarray, list: List[np.ndarray]) -> bool:

    for item in list:
        if np.array_equal(element, item):
            return True

    return False

def manhattanDistance(element1: np.ndarray, element2: np.ndarray) -> int:
    dist = np.sum(np.abs(element1 - element2))
    return dist


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
    

    def Update(self, action, control_type):

        if control_type == "relative":
            self.RotateDirection(action)
        elif control_type == "absolute":
            absolute_action = DIRECTIONS[np.argmax(action)]
            self.direction = absolute_action
        self.head = self.body[0] + self.direction
        self.body.insert(0, self.head)
        

        if self.addSegment:
            self.addSegment = False
        else:
            self.body.pop()

    def Reset(self):
        start_rand_n = np.random.randint(0, 4)
        start_direction = DIRECTIONS[start_rand_n]
        start_x = np.random.randint(3, cell_count-2)
        start_y = np.random.randint(3, cell_count-2)
        self.head = np.array([start_x, start_y])
        self.body = [self.head, self.head + start_direction, self.head + start_direction * 2]
        self.direction = np.array([1, 0])

    def RotateDirection(self, action):
        if action == LEFT:
            self.direction =  self.direction @ np.array([[0, -1], [1, 0]])
        elif action == STRAIGHT:
            pass
        elif action == RIGHT:
            self.direction =  self.direction @ np.array([[0, 1], [-1, 0]])

        

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

    def __init__(self, control_type, check_connected=False):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.frame_iteration = 0
        self.score = 0
        self.done = False
        self.control_type = control_type
        self.check_connected = check_connected
        
        

    def Reset(self):
        self.snake.Reset()
        self.food.position = self.food.GenerateRandomPos(self.snake.body)
        self.frame_iteration = 0
        self.score = 0
        self.done = False


    def Draw(self):
        self.food.Draw()
        self.snake.Draw()
    
    def Step(self, action):
        self.frame_iteration += 1
        self.reward = 0

        screen.fill(colorGreen)
        self.Draw()
        pygame.display.flip()

        if self.check_connected:
            self.CheckConnected()
        self.snake.Update(action, self.control_type)
        self.CheckCollisionWithFood()
        self.CheckCollisionWithEdges()
        self.CheckCollisionWithTail()
        self.FoodDistanceReward()

        if self.frame_iteration > 100 * len(self.snake.body):
            self.GameOver()

        return self.reward, self.done, self.score
    
    def FoodDistanceReward(self):
        currentDist = manhattanDistance(self.snake.body[0], self.food.position)
        prevDist = manhattanDistance(self.snake.body[1], self.food.position)
        
        if currentDist < prevDist:
            self.reward += 2

    def Occupance_Grid(self):
        
        grid = np.zeros((cell_count,cell_count), dtype=int)
        
        for part in self.snake.body:
            grid[part[0], part[1]] = 1
        
        return grid

    def CheckConnected(self):
        occupance_grid = self.Occupance_Grid()

        free_connected = check_reachable(occupance_grid)

        if not free_connected:
            self.reward -= 5


    def CheckCollisionWithFood(self):

        if np.array_equal(self.snake.body[0], self.food.position):
            self.food.position = self.food.GenerateRandomPos(self.snake.body)
            self.snake.addSegment = True
            self.reward = 10
            self.score += 1

    def CheckCollisionWithEdges(self):

        if self.snake.body[0][0] == -1 or self.snake.body[0][0] == cell_count or self.snake.body[0][1] == -1 or self.snake.body[0][1] == cell_count:
            self.GameOver()
    
    def CheckCollisionWithTail(self):

        headlessBody = self.snake.body[1::]
        if(elementInList(self.snake.body[0], headlessBody)):
            self.GameOver()

    def CheckDanger(self, point: np.ndarray) -> bool:
        tailHit = elementInList(point, self.snake.body)
        edgeHit = point[0] == -1 or point[0] == cell_count or point[1] == -1 or point[1] == cell_count

        return tailHit or edgeHit


    def GameOver(self):
        self.reward = -30
        self.done = True
        self.food.position = self.food.GenerateRandomPos(self.snake.body)
        self.snake.Reset()
        


if __name__ == "__main__":
    
    game = Game()

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

                reward, done, score = game.Step(action)

                print("reward:", reward, ", done:", done, ", score:", score)

                screen.fill(colorGreen)
                game.snake.Draw()
                game.food.Draw()

            pygame.display.flip()
    pygame.quit()