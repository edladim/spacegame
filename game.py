import pygame as pg
import math
import random
import sys
pg.init()

screen_width = 800
screen_height = 700

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Game")

clock = pg.time.Clock()


class Squere:
    def __init__(self, x_position, y_position, width, height, speed):
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.speed = speed
        self.diagonalSpeed = self.speed / 2 * math.sqrt(2)

    def rect(self):
        return pg.Rect(self.x_position, self.y_position, self.width, self.height)

    def center(self):
        x = self.x_position + self.width // 2
        y = self.y_position + self.height // 2
        return (x, y)

    def move_to(self, x_position, y_position):
        if x_position < 0:
            x_position = 0
        elif x_position + self.width > screen_width:
            x_position = screen_width - self.width

        if y_position < 0:
            y_position = 0
        elif y_position + self.height > screen_height:
            y_position = screen_height - self.height

        self.x_position = x_position
        self.y_position = y_position

class Player(Squere):
    def __init__(self, x_position, y_position, width, height, speed):
        super().__init__(x_position, y_position, width, height, speed)
        self.shoot_cooldown = 0

    def shoot(self, bullets):
        if self.shoot_cooldown == 0:
            bullet_pos = list(self.center())
            bullet = Bullet(bullet_pos[0], bullet_pos[1])
            bullets.append(bullet)
            self.shoot_cooldown = 20

class Enemy(Squere):
    def __init__(self, x_position, y_position, width, height, speed):
        super().__init__(x_position, y_position, width, height, speed)

    def update(self, enemies):
        self.y_position += self.speed
        if self.y_position + self.height > screen_height:
            enemies.remove(self)
            run = False  # add this line to stop the game loop
            screen.fill((0, 0, 0))  # clear the screen
            font = pg.font.Font(None, 36)
            text = font.render("Game Over", True, (255, 255, 255))
            screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
            pg.display.update()
            pg.time.wait(2000)  # wait for 2 seconds before quitting
            pg.quit()
            sys.exit()


class Bullet(Squere):
    def __init__(self, x_position, y_position, length = 10, speed = 15):
        super().__init__(x_position, y_position, length, length, speed)
        self.speed = speed
        self.length = length

    def update(self, bullets):
        self.y_position -= self.speed
        if self.y_position + self.length < 0 or self.y_position - self.length > screen_height:
            bullets.remove(self)

plr = Player(400, 600, 50, 50, 10)


bullets = []
enemies = []
time_counter = 0

run = True
while run:
    screen.fill((0, 0, 0))

    pg.draw.rect(screen, (255, 0, 0), plr.rect())

    key = pg.key.get_pressed()
    if key[pg.K_a]:
        if key[pg.K_w]:
            plr.move_to(plr.x_position - (plr.diagonalSpeed), plr.y_position - plr.diagonalSpeed)
        elif key[pg.K_s]:
            plr.move_to(plr.x_position - plr.diagonalSpeed, plr.y_position + plr.diagonalSpeed)
        else:
            plr.move_to(plr.x_position - plr.speed, plr.y_position)
    elif key[pg.K_d]:
        if key[pg.K_w]:
            plr.move_to(plr.x_position + plr.diagonalSpeed, plr.y_position - plr.diagonalSpeed)
        elif key[pg.K_s]:
            plr.move_to(plr.x_position + plr.diagonalSpeed, plr.y_position + plr.diagonalSpeed)
        else:
            plr.move_to(plr.x_position + plr.speed, plr.y_position)
    elif key[pg.K_w]:
        plr.move_to(plr.x_position, plr.y_position - plr.speed)
    elif key[pg.K_s]:
        plr.move_to(plr.x_position, plr.y_position + plr.speed)

    if key[pg.K_p]:
        plr.shoot(bullets)
    

    for bullet in bullets:
        pg.draw.rect(screen, (0, 0, 255), bullet.rect())
        bullet.update(bullets)

        
    if time_counter < 100:
        time_counter += 1
    else:
        enemy = Enemy(random.randint(0, screen_width - 50), 0, 50, 50, 10)
        enemies.append(enemy)
        time_counter = 0

    for enemy in enemies:
        pg.draw.rect(screen, (0, 255, 0), enemy.rect())

    for i, enemy in enumerate(enemies):
        enemy_collision = enemy.rect().colliderect(plr.rect())
        if enemy_collision:
            enemies.pop(i)
            print("Game Over")

    for enemy in enemies:
        for bullet in bullets:
            if enemy.rect().colliderect(bullet.rect()):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    for enemy in enemies:
        enemy.update(enemies)


    if plr.shoot_cooldown > 0:
        plr.shoot_cooldown -= 1
    
    pg.display.update()
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

pg.quit()