import pygame, sys
from pygame.math import Vector2
from config import *
from food import Food
from snake import Snake



class Game:
    '''Define the game class that contains the game state and elements
    '''
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.hscore = 0
        self.lives = 1
        self.snake_speed = 10
        self.count_food=0  
        
    def draw_lives(self):
        '''Draw the lives on the screen'''
        lives_surface = score_font.render(f"Lives: {self.lives}", True, DARK_GREEN)
        screen.blit(lives_surface, (cell_size * cell_number - 50, OFFSET - 40))

    def draw_time_rectangle(self):
        '''Draw the time rectangle on the screen'''
        if self.food.is_special:
            self.food.special_food_timer-=1/60
            remain_time_ratio=self.food.special_food_timer/8
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(OFFSET - 5, screen.get_height() - 45, (screen.get_width() - 2 * (OFFSET - 5)) * remain_time_ratio, 30))
    
    def draw_grass(self):
        '''Draw the grass on the screen'''
        grass_color = (167, 209, 61)

        for x in range(cell_number):
            for y in range(cell_number):
                rect = pygame.Rect(
                    OFFSET + x * cell_size, OFFSET + y * cell_size, cell_size, cell_size
                )
                if (x + y) % 2 == 0:
                    pygame.draw.rect(screen, grass_color, rect)
                else:
                    pygame.draw.rect(screen, "white", rect)

    def draw_score_highscore(self):
        '''Draw the score and high score on the screen'''
        score_position = (OFFSET - 5, OFFSET - 40)
        score_surface = score_font.render(f"Score:   {game.score}", True, DARK_GREEN)
        screen.blit(score_surface, score_position)

        food_position = (2 * score_position[0] + 25, OFFSET - 40)
        screen.blit(food_surface, food_position)

        if self.hscore < self.score:
            self.hscore = self.score

        hscore_position = (score_position[0] * 4, OFFSET - 40)
        hscore_surface = score_font.render(
            f"High Score:   {game.hscore}", True, DARK_GREEN
        )
        screen.blit(hscore_surface, hscore_position)
        food_position = (hscore_position[0] + 155, OFFSET - 40)
        screen.blit(food_surface, food_position)
    def draw_endgame_message(self):
        '''Draw the end game message on the screen'''

        endgame_font = pygame.font.Font(None, 35)
        endgame_text = endgame_font.render(
            "Game Over! Press ENTER to play again or ESC to exit!", True, DARK_GREEN
        )
        screen.blit(endgame_text, (OFFSET - 5, OFFSET + cell_size * cell_number + 20))
    def draw(self):
        '''Draw the game elements on the screen'''
        self.draw_grass()
        self.food.draw_food()
        self.draw_score_highscore()
        self.draw_lives()
        
        if self.state=="RUNNING":
            self.draw_time_rectangle()
        if self.state == "STOPPED":
            self.snake.draw_snake_history()
            self.draw_endgame_message() 
        else:
            self.snake.draw_snake()
        
    def check_collision_with_food(self):
        '''Check if the snake collides with the food'''
        if self.food.position == self.snake.body[0]:
            self.snake.add_segment = True
            if self.food.is_special:
                self.lives += 1
                self.score += 3
                self.food.is_special = False
            else:
                self.score += 1
                self.count_food+=1

            self.food.position = self.food.generate_random_pos(self.snake.body)
            if self.count_food % 2 == 0 and self.count_food!=0:    # khi ăn đủ 4 thức ăn thường thì xuất hiện thức ăn đặc biệt
                self.food.generate_special_food(self.snake.body)
                self.count_food=0
            self.snake.eat_sound.play()

    def check_collision(self):
        '''
        Check if the snake collides with the wall or itself
        '''
        headless_body = self.snake.body[1:]
        if (
            not 0 <= self.snake.body[0].x < cell_number
            or not 0 <= self.snake.body[0].y < cell_number
            or self.snake.body[0] in headless_body
        ):           
            self.lives -= 1           
            self.snake.wall_sound.play()
            if self.lives <= 0:
                self.game_over()
            else:
                self.snake.reset()
                
                

    def game_over(self):
        ''' Game over state '''
        self.state = "STOPPED"
        self.count_food=0
        self.snake.wall_sound.play()


    def update(self):
        ''' Update the game state'''
        if self.snake.next_direction:
            self.snake.direction = self.snake.next_direction
            self.snake.next_direction = None       
        if self.state == "RUNNING":
            self.snake.update(self.snake_speed)
            self.food.update(self.snake.body)
            self.check_collision_with_food()
            self.check_collision()
            self.snake_speed = 10*(1 + self.score //3)

    def handle_key_events(self, event):
        '''Handle the key events for the game'''
        if event.type == pygame.KEYDOWN:
            self.snake.started = True
            if self.state == "STOPPED":
                if (
                    event.key == pygame.K_RETURN
                ):  # Người chơi nhấn ENTER để bắt đầu lại trò chơi
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:  # Người chơi nhấn ESC để thoát
                    pygame.quit()
                    sys.exit()
            else:  # Trò chơi đang chạy
                if event.key == pygame.K_UP and self.snake.direction != Vector2(0, 1):
                    self.snake.next_direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and self.snake.direction != Vector2(
                    0, -1
                ):
                    self.snake.next_direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and self.snake.direction != Vector2(1, 0):
                    self.snake.next_direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and self.snake.direction != Vector2(
                    -1, 0
                ):
                    self.snake.next_direction = Vector2(1, 0)

    def reset_game(self):
        '''Reset the game state'''
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.food.is_special = False
        self.state = "RUNNING"
        self.score = 0
        self.lives=1

game = Game()
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            game.handle_key_events(event)

    screen.fill(GREEN)
    pygame.draw.rect(
        screen,
        DARK_GREEN,
        (
            OFFSET - 5,
            OFFSET - 5,
            cell_size * cell_number + 10,
            cell_size * cell_number + 10,
        ),
        5,
    )
    game.draw()
    pygame.display.update()
    fps.tick(100)
