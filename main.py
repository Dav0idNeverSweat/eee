from pygame import*
from abc import ABC, abstractmethod
from time import sleep

init()
window = display.set_mode((700, 500))
display.set_caption('Ball Game :D')
clock =  time.Clock()
window.fill((255, 255, 255))

mixer.music.load('Background_music.mp3')
mixer.music.set_volume(0.25)

Game_over  = mixer.Sound("Game_over.mp3")
Game_start = mixer.Sound("Game_start.mp3")
Bounce_sfx = mixer.Sound("BallBounceSFX.mp3") # SFX
#fire_sfx.set_volume(1) # Volume

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, img="racket.png"):
        super().__init__()
        self.speed = speed
        try:
            self.width = width
            self.height = height
            self.image = transform.scale(image.load(img), (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        except:
            self.rect = Rect(x, y, width, height)

    def reset(self):
        try:
            window.blit(self.image, (self.rect.x, self.rect.y))
        except:
            draw.rect(window, self.image[0], Rect(self.rect.x, self.rect.y, self.width + 10, self.height + 10))
            draw.rect(window, self.image[1], Rect(self.rect.x + 5, self.rect.y + 5, self.width, self.height))


    def write_text(self, text, font_size, colour, x, y):
        txt_font = font.Font(None, font_size)
        text = txt_font.render(text, True, colour)
        window.blit(text, (x, y))

class Player(GameSprite):
    @abstractmethod
    def update(self):
        pass

class Player1(Player):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        if keys[K_a]:
            self.rect.y -= self.speed
        if keys[K_d]:
            self.rect.y += self.speed

class Player2(Player):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed
        if keys[K_LEFT]:
            self.rect.y -= self.speed
        if keys[K_RIGHT]:
            self.rect.y += self.speed

class Ball(GameSprite):
    def add_speed(self):
        self.x_speed = self.speed * -1
        self.y_speed = self.speed
    
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

def finalResult(result):
    window.fill((255, 255, 255))
    if result == 'Win1':
        tfont = font.Font(None, 100)
        text = tfont.render('PLAYER 1 WIN!', True, (255, 193, 7))
        window.blit(text, (180, 200))
    elif result == 'Win2':
        tfont = font.Font(None, 100)
        text = tfont.render('PLAYER 2 WIN!', True, (255, 193, 7))
        window.blit(text, (180, 200))
    elif result == 'Tie':
        tfont = font.Font(None, 100)
        text = tfont.render('TIE?', True, (255, 193, 7))
        window.blit(text, (160, 200))
    else:
        raise Exception('Unknown event')

player1 = Player1(70, 219, 62, 64, 5)
player2 = Player2(630, 219, 62, 64, 5)
ball    = Ball(350, 250, 50, 50, 5, "ball.png")
sound_button = GameSprite(625, 0, 50, 50, 0, "Sound On.png")
sound   = True
score1  = 0
score2  = 0
max_score = 5
bg_sfx  = 0
ball.add_speed()

running = True

if sound:
    mixer.music.play()
    Game_start.play()
while running:
    for bevent in event.get():
        if bevent.type == QUIT:
            quit()
        if bevent.type == MOUSEBUTTONDOWN and bevent.button == 1:
            if sound_button.rect.collidepoint(mouse.get_pos()):
                sound = not sound
                if not sound:
                    mixer.music.pause()
                elif sound:
                    mixer.music.play()

    if sound:
        sound_button.image = transform.scale(image.load("Sound On.png"), (sound_button.width, sound_button.height))
    elif sound == False:
        sound_button.image = transform.scale(image.load("Sound Off.png"), (sound_button.width, sound_button.height))
    # score event end
    if score1 == max_score or score2 == max_score:
        running = False
    
    # collision event
    if sprite.collide_rect(player1, ball) or sprite.collide_rect(player2, ball):
        ball.x_speed *= -1
        ball.y_speed *= -1
        if sound:
            Bounce_sfx.play()
    
    if ball.rect.y <= 0 or ball.rect.y >= 500:
        ball.y_speed *= -1
        if sound:
            Bounce_sfx.play()

    if ball.rect.x <= 0 or ball.rect.x >= 700:
        ball.x_speed *= -1
        if sound:
            Bounce_sfx.play()

        # Score update
        if ball.rect.x <= 0:
            score1 += 1
        elif ball.rect.x >= 700:
            score2 += 1
    
    # player update/reset, score update(text)
    player1.update()
    player2.update()
    ball.update()

    window.fill((255, 255, 255))

    player1.reset()
    player2.reset()
    ball.reset()
    sound_button.reset()
    player1.write_text("Player 1's score: " + str(score1) + r"/" + str(max_score), 24, (0, 0, 0), 10, 10)
    player2.write_text("Player 2's score: " + str(score2) + r"/" + str(max_score), 24, (0, 0, 0), 10, 40)
    
    display.update()
    clock.tick(60)

# sfx for the loser player
if sound:
    mixer.music.stop()
    Game_over.play()

running = True
while running:
    for bevent in event.get():
        if bevent.type == QUIT:
            quit()
    if score1 >= max_score:
        finalResult('Win1')
    elif score2 >= max_score:
        finalResult('Win2')
    else:
        raise Exception('Unknown event')
    
    display.update()
    clock.tick(60)