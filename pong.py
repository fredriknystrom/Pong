import pygame
import time
import sys

pygame.init()

# Screen setup
SIZE = (WIDTH, HEIGHT) = (1200, 800)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong")
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
SCORE_FONT = pygame.font.SysFont('arial', 30)
COUNT_FONT = pygame.font.SysFont('arial', 60)
WINNER_FONT = pygame.font.SysFont('arial', 80)

# Create ball object
class Ball():

    def __init__(self, speed_x, speed_y, diameter):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.diameter = diameter
        self.rect = pygame.Rect(WIDTH/2 - self.diameter/2, HEIGHT/2 - self.diameter/2,
                                self.diameter, self.diameter)

# Create player object
class Player():

    def __init__(self, speed, width, height, score, x):
        self.speed = speed
        self.width = width
        self.height = height
        self.score = score
        self.rect = pygame.Rect(x, HEIGHT/2 - self.height/2, self.width, self.height)

# Decide ball direction and move the ball
def ball_movement(ball, red_player, blue_player):
   
    ball.rect.x += ball.speed_x
    ball.rect.y += ball.speed_y
    if ball.rect.x < 0:
        blue_player.score +=1
        if blue_player.score < 5:
            respawn_ball(ball, red_player, blue_player)
    if ball.rect.right > WIDTH:
        red_player.score +=1
        if red_player.score < 5:
            respawn_ball(ball, red_player, blue_player)
       
    if ball.rect.y < 0 or ball.rect.bottom > HEIGHT:
        ball.speed_y *= -1
    
    if ball.rect.colliderect(blue_player.rect) or ball.rect.colliderect(red_player.rect):
            ball.speed_x *= -1

# Respawns ball in middle and resetplaer position with a three second countdown
def respawn_ball(ball, red_player, blue_player):
    ball.rect.x = WIDTH/2 - ball.diameter/2
    ball.rect.y = HEIGHT/2 - ball.diameter/2
    red_player.rect.y = HEIGHT/2 - red_player.height/2
    blue_player.rect.y = HEIGHT/2 - blue_player.height/2
    for i in range(3, 0, -1):
        draw(ball, red_player, blue_player)
        countdown = COUNT_FONT.render(str(i), 1, YELLOW)
        SCREEN.blit(countdown, (WIDTH/2 - countdown.get_width()/2, HEIGHT/2 - countdown.get_height()/2 -
                                2 * ball.diameter))
        pygame.display.update()
        time.sleep(1)

# Move players (input dependent)
def player_movement(keys_pressed, red_player, blue_player):

    if keys_pressed[pygame.K_w] and red_player.rect.y - red_player.speed >=0:
            red_player.rect.y -= red_player.speed
    if keys_pressed[pygame.K_s] and red_player.rect.bottom + red_player.speed <= HEIGHT:
            red_player.rect.y += red_player.speed

    if keys_pressed[pygame.K_UP] and blue_player.rect.y - blue_player.speed >=0:
                blue_player.rect.y -= blue_player.speed
    if keys_pressed[pygame.K_DOWN] and blue_player.rect.bottom + blue_player.speed <= HEIGHT:
            blue_player.rect.y += blue_player.speed

# Draw visuals
def draw(ball, red_player, blue_player):
    SCREEN.fill(BLACK)

    pygame.draw.ellipse(SCREEN, YELLOW, ball.rect)
    pygame.draw.rect(SCREEN, RED, red_player.rect)
    pygame.draw.rect(SCREEN, BLUE, blue_player.rect)
    pygame.draw.aaline(SCREEN, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    red_score = SCORE_FONT.render(f"Red Score: {red_player.score}", 1, RED)
    SCREEN.blit(red_score, (red_player.rect.right + red_player.width, red_player.rect.x))
    blue_score = SCORE_FONT.render(f"Blue Score: {blue_player.score}", 1, BLUE)
    SCREEN.blit(blue_score, (blue_player.rect.left - blue_player.width - blue_score.get_width(),
                             blue_player.width))
    pygame.display.update()

# Check if there is a winner
def isWinner(red_player, blue_player):
    if red_player.score >= 5:
        winner_text = WINNER_FONT.render("Red Player Won The Game", 1, RED)
        SCREEN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, 
                    HEIGHT/2 - winner_text.get_height()/2))
        return True
    if blue_player.score >= 5:
        winner_text = WINNER_FONT.render("Blue Player Won The Game", 1, BLUE)
        SCREEN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, 
                    HEIGHT/2 - winner_text.get_height()/2))
        return True
    return False


def main():

    clock = pygame.time.Clock()

    ball = Ball(5, 5, 30)
    red_player = Player(5, 20, 120, 0, 20)
    blue_player = Player(5, 20, 120, 0, WIDTH - 40)

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        ball_movement(ball, red_player, blue_player)
        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, red_player, blue_player)
        
        draw(ball, red_player, blue_player)

        if isWinner(red_player, blue_player):
            pygame.display.update()
            running = False

    time.sleep(2)
    main()


if __name__ == "__main__":
    main()