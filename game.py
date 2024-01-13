import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((1200, 900))

pygame.display.set_caption('ロビンフットゲーム')

# Yumi
yumiImg = pygame.image.load('yumi.png')
yumiX, yumiY = 900, 800
yumiX_change = 0

# Ringo
ringoImg = pygame.image.load('ringo.png')
ringoX = random.randint(0, 736)
ringoY = random.randint(50, 150)
ringoX_change, ringoY_change = 4, 40

# Ya
yaImg = pygame.image.load('ya.png')
yaX, yaY = 0, 800
yaX_change, yaY_change = 0, 6
ya_state = 'ready'

# Score
score_value = 0

def yumi(x, y):
    screen.blit(yumiImg, (x, y))

def ringo(x, y):
    screen.blit(ringoImg, (x, y))

def hit_ya(x, y):
    global ya_state
    ya_state = 'fire'
    screen.blit(yaImg, (x + 16, y + 10))

def isCollision(ringoX, ringoY, yaX, yaY):
    distance = math.sqrt(math.pow(ringoX - yaX, 2) + math.pow(ringoY - yaY, 2))
    if distance < 27:
        return True
    else:
        return False
    
# ゲームオーバー用フォント
game_over_font = pygame.font.SysFont(None, 64)

running = True
game_over = False
game_over_timer = 0

while running:
    screen.fill((150, 255, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                yumiX_change = -3
            if event.key == pygame.K_RIGHT:
                yumiX_change = 3
            if event.key == pygame.K_SPACE:
                if ya_state is 'ready':
                    yaX = yumiX
                    hit_ya(yaX, yaY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                yumiX_change = 0
    # Yumi
    yumiX += yumiX_change
    if yumiX <= 0:
        yumiX = 0
    elif yumiX >= 1140:
        yumiX = 1140

    # ringo
    if ringoY > 700:
        game_over = True
    ringoX += ringoX_change
    if ringoX <= 0: #左端に来たら
        ringoX_change = 3
        ringoY += ringoY_change
    elif ringoX >=1170: #右端に来たら
        ringoX_change = -3
        ringoY += ringoY_change
    
    # ゲームオーバーの場合
    if game_over:
        ringoX_change = 0
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (400, 400))
        game_over_timer += 1

        if game_over_timer == 360:
            running = False
            game_over = False
            game_over_timer = 0
    else:

        collision = isCollision(ringoX, ringoY, yaX, yaY)
    if collision:
        yaY = 800
        ya_state = 'ready'
        score_value += 1
        ringoX = random.randint(0, 736)
        ringoY = random.randint(50, 150)

    # Ya ugoki
    if yaY <=0:
        yaY = 800 
        ya_state = 'ready'

    if ya_state is 'fire':
        hit_ya(yaX, yaY)
        yaY -= yaY_change  

    # Score
    font = pygame.font.SysFont(None, 32) 
    score = font.render(f"Score : {str(score_value)}", True, (255,255,255))
    screen.blit(score, (20,50))

    yumi(yumiX, yumiY)
    ringo(ringoX, ringoY)

    pygame.display.update()
