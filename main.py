import pygame, random, os, time
from pygame.locals import *

# Constatnts 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue =(0,0,255)
WIDTH  = 600
HEIGHT = 400
FPS = 60
random_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
# constants for font and 
pygame.font.init()
SCORE_FONT = pygame.font.SysFont("Comic Sans MS", 20)
LEVEL_FONT = pygame.font.SysFont("Comic Sans MS", 20)
GAME_OVER_FONT = pygame.font.SysFont("Comic Sans MS", 30)

# Screen methods and time 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ball_to_paddle = pygame.mixer.Sound("ball_paddle.wav")
ball_to_walls = pygame.mixer.Sound("ball_walls.wav")
powr_up = pygame.mixer.Sound("power_up.wav")

class Ball(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ball.png").convert()
        self.image.set_colorkey(black)
        self.image = pygame.transform.scale(self.image,(20,20))
        #self.image = pygame.Surface((10,10))
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT /4 - 30)
        self.x_speed = random.randrange(-3, 3)
        self.y_speed = 3
        self.rotation = 0
        self.y_direction = "down"
        self.score = 0
        self.total_score = 1
        self.score_text = SCORE_FONT.render("score: "+str(self.score),
         False,(green))
        self.game_over_text = GAME_OVER_FONT.render("Game over", False,(red))
        self.game = "on"
        self.level_counter = 1 
        self.level_text = LEVEL_FONT.render("Level: "+str(self.level_counter),True,(blue)) 

    def update(self):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        # Using rect.collide in a most simplest way instead of using sprite Group collission method
        # im also going to use a flag (up, down) to clean up the movement from possible errors 
        # Logic for interaction between ball and the paddle 
        if self.y_direction == "down" and self.rect.colliderect (player.rect):
            #self.image.fill(red)
            #player.image.fill(blue)
            ball_to_paddle.play()
            player.rect.y += 5
            self.score +=1
            self.total_score +=1
            self.score_text = score_text = SCORE_FONT.render("score: "+str(self.score), True,(green))
            self.y_speed *= -1
            self.y_direction = "up"
        if self.y_direction == "up" and self.rect.top <= 0:
            ball_to_walls.play()
            self.x_speed = self.get_random_move()
            self.y_speed *= -1
            self.y_direction = "down"
        # Logic for side movement restriction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.x_speed *= -1
            ball_to_walls.play()
        if self.y_direction == "down"and self.rect.top > HEIGHT:
            self.game = "off"
        if self.score == 10:
            self.level_counter += 1
            self.level_text = LEVEL_FONT.render("Level: "+str(self.level_counter),True,(blue))
            self.score = 0
            self.y_speed -= 1
            player.left_speed -= 1
            player.right_speed += 1
           
    def get_random_move(self):
        return random.randrange(-4,4)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width_size = 80
        self.height_size = 5
        self.image = pygame.image.load("paddle.png").convert()
        self.image.set_colorkey(black)
        self.image = pygame.transform.scale(self.image,(self.width_size, self.height_size))
        #self.image = pygame.Surface((self.width_size, self.height_size))
        #self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center =(WIDTH/2, HEIGHT/1 -10)
        self.x_speed = 0
        self.x_stop= 0 
        self.left_speed = -4
        self.right_speed = 4 


    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x_speed = self.left_speed
        if keystate[pygame.K_RIGHT]:
            self.x_speed = self.right_speed
        if keystate[pygame.K_DOWN]:
            self.x_speed = self.x_stop
        self.rect.x += self.x_speed
        if self.rect.left <0 :
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.y == 393:
            self.rect.y = 388

class Power_up(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("p.png").convert()
        self.image.set_colorkey(black)
        self.image = pygame.transform.scale(self.image,(1,10))
        #self.image = pygame.Surface((5,5))
        #self.image.fill(random_color)
        self.rect = self.image.get_rect()
        self.rect.center =(random.randrange(0, WIDTH), 10)
        self.y_speed = (random.randrange(1,3))
        self.x_speed = (random.choice((10, -10)))
    
    def update(self):
        self.rect.y += self.y_speed
        if self.rect.colliderect (player.rect):
            self.explode()
            powr_up.play()
            player.width_size += 5
            player.image = pygame.image.load("paddle.png").convert()
            player.image.set_colorkey(black)
            player.image = pygame.transform.scale(player.image,(player.width_size, player.height_size))
            #player.image.fill(blue)
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()

    def explode(self):
        self.image = pygame.Surface((1,1))
        self.image.fill(green)
        self.y_speed *= -10
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()
        if self.rect.y <0 or self.rect.y >HEIGHT:
            self.kill()



# Objects
power_ups = pygame.sprite.Group()
all_s = pygame.sprite.Group()

player = Player()
for power_up in range(2):
    power_ups.add(Power_up(player))
power_up = Power_up(player)

ball = Ball(player)

all_s.add(player)
all_s.add(ball)
for power_up in power_ups:
    all_s.add(power_up)

#power_ups.add(power_up)
def main():
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if ball.game == "off":
            screen.blit(ball.game_over_text,(WIDTH/2, HEIGHT/2))
        for power_up in power_ups:
            spawn = random.randrange(1, 10)
            if len(power_ups)< 3 or len(power_ups) == 0:
                power_ups.add(Power_up(player))
        if player.width_size >= 95:
            player.width_size = 80
            
        all_s.update()
        power_ups.update()

        screen.fill(black)
        screen.blit(ball.score_text,(10,10))
        screen.blit(ball.level_text,(500, 10))
        all_s.draw(screen)
        power_ups.draw(screen)
        if ball.game == "off":
            screen.blit(ball.game_over_text,(220,150))
            running = False

        pygame.display.flip()

    pygame.quit()
if __name__ == "__main__":
    main()
