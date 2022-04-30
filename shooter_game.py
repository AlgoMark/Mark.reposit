from pygame import *
from random import randint

points = 0
falls = 0

font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 100)

lose = font2.render('You lose!', True, (255, 0, 0))


width = 700
height = 500
window = display.set_mode((width, height))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'),(700,500))

class my_sprite(sprite.Sprite):
    def __init__(self,picture,x,y,w,h,speed):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class hero(my_sprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed
    def fire(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            bullet0 = bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
            bullets.add(bullet0)
            fire.play()

class enemy(my_sprite):
    def update(self):
        global falls
        if self.rect.y < width:
            self.rect.y += self.speed
        else:
            self.rect.x = randint(25, width-25)
            self.rect.y = 0
            falls += 1
class bullet(my_sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class asteroid(enemy):
    def update(self):
        if self.rect.x < height:
            self.rect.x += self.speed
        else:
            self.rect.y = randint(100, height-50)
            self.rect.x = 0



rocket = hero('rocket.png', 325, 425,75,75, 3)
ufo1 = enemy('ufo.png', randint(25, width-25), 0, 80, 50, randint(1,2))
ufo2 = enemy('ufo.png', randint(25, width-25), 0, 80, 50, randint(1,2))
ufo3 = enemy('ufo.png', randint(25, width-25), 0, 80, 50, randint(1,2))
ufo4 = enemy('ufo.png', randint(25, width-25), 0, 80, 50, randint(1,2))
ufo5 = enemy('ufo.png', randint(25, width-25), 0, 80, 50, randint(1,2))
asteroid1 = asteroid('asteroid.png', 0, randint(100, height-150), 80, 50, 1)

rocket_x = rocket.rect.centerx
rocket_y = rocket.rect.top

ufoes = sprite.Group()
ufoes.add(ufo1)
ufoes.add(ufo2)
ufoes.add(ufo3)
ufoes.add(ufo4)
ufoes.add(ufo5)

bullets = sprite.Group()
asteroids = sprite.Group()
asteroids.add(asteroid1)

clock = time.Clock()
FPS = 30
clock.tick(FPS)

mixer.init()
fire = mixer.Sound('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()

finish = False

game_cicle = True
while game_cicle == True:
    
    for i in event.get():
        if i.type == QUIT:
            game_cicle = False
    if not finish:
        window.blit(background,(0,0))

        points_label = font1.render('Счёт:'+ str(points), True, (0, 255, 0))
        falls_label = font1.render('Пропущено:'+ str(falls), True, (0, 255, 0))

        window.blit(points_label, (25, 25))
        window.blit(falls_label, (25, 75))
    
        rocket.move()
        rocket.fire()
        ufoes.update()
        bullets.update()
        asteroids.update()

        rocket.reset()
        ufoes.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprites_list1 = sprite.spritecollide(rocket,ufoes,False)
        sprites_list2 = sprite.spritecollide(rocket,asteroids,False)
        l_sprite1 = len(sprites_list1)
        l_sprite2 = len(sprites_list2)
        sprite_groupes_list1 = sprite.groupcollide(ufoes,bullets,True,True)
        sprite_groupes_list2 = sprite.groupcollide(asteroids,bullets,False,True)

        for a in sprite_groupes_list1:
            points += 1
            ufo = enemy('ufo.png', randint(25, width-25), 0, 80, 50, randint(1,2))
            ufoes.add(ufo)

        if falls >= 3 or l_sprite1 > 0 or l_sprite2 > 0:
            lose = font2.render('You lose!', True, (255, 0, 0))
            window.blit(lose, (250, 200))
            finish = True

        if points >= 15:
            win = font2.render('You win!', True, (255, 215, 0))
            window.blit(win, (250, 200))
            finish = True

    display.update()