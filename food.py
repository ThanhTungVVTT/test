from config import *
import random


class Food:
    '''Define the food class that contains the food position and graphics'''
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)
        self.is_special = False
        self.special_food_timer=8 # thức ăn đặc biệt tồn tại trong 8 giây
        self.frame_counter=0 

    def draw_food(self):
        '''Draw the food on the screen'''
        if self.is_special:
            screen.blit(
                special_food_surface,
                (
                    OFFSET + self.position.x * cell_size,
                    OFFSET + self.position.y * cell_size,
                    cell_size,
                    cell_size,
                ),
            )
        else:
            food_rect = pygame.Rect(
                OFFSET + self.position.x * cell_size,
                OFFSET + self.position.y * cell_size,
                cell_size,
                cell_size,
            )

            screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        '''Generate a random cell position for the food'''
        x = random.randint(0, cell_number - 1)
        y = random.randint(0, cell_number - 1)
        return Vector2(x, y)

    def generate_special_food(self, snake_body):
        '''Generate a special food that gives extra lives'''
        self.is_special = True
        self.special_food_timer=8
        self.position = self.generate_random_pos(snake_body)
        

    def generate_random_pos(self, snake_body):
        '''Generate a random position for the food'''
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position
    def update(self,snake_body):
        '''Update the food state'''
        if self.is_special:
            self.frame_counter+=1
            if self.frame_counter>=60:
                self.special_food_timer-=1
                self.frame_counter=0
            if self.special_food_timer<=0:
                self.is_special=False
                self.position=self.generate_random_pos(snake_body)