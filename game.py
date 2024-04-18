import pygame as pg
import math
import random
import sys
pg.init()

screen_width = 600
screen_height = 800

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Game")

clock = pg.time.Clock()


class Square:
    def __init__(self, x_position, y_position, width, height, speed):
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.speed = speed
        self.diagonal_speed = self.speed / 2 * math.sqrt(2)  

    def rect(self):
        return pg.Rect(self.x_position, self.y_position, self.width, self.height)

    def center(self):
        x = self.x_position + self.width // 2
        y = self.y_position + self.height // 2
        return (x, y)

    def move_x(self):
        self.x_position += self.speed
    
    def move_y(self):
        self.y_position += self.speed

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
    
    def border_colide(self):
        if self.y_position + self.height < 0 or self.y_position > screen_height:
            return True
        elif self.x_position + self.width < 0 or self.x_position > screen_width:
            return True


class Player(Square):
    def __init__(self, x_position, y_position, width, height, speed):
        super().__init__(x_position, y_position, width, height, speed)
        self.shoot_cooldown = 0
        self.shoot_three = False 

    def shoot(self, bullets):
        if self.shoot_cooldown == 0:
            if not self.shoot_three:
                plr_center = list(self.center())
                #blt_center = list(bullet)
                bullet = Bullet(plr_center[0] - 5, self.y_position)
                bullets.append(bullet)
                self.shoot_cooldown = 20
            else:
                for i in range(3):
                    plr_center = list(self.center())
                    plr_center[0] += (i - 1) * 20
                    bullet = Bullet(plr_center[0] - 5, self.y_position)
                    bullets.append(bullet)
                self.shoot_cooldown = 20

class Enemy(Square):
    def __init__(self, x_position, y_position, width, height, speed):
        super().__init__(x_position, y_position, width, height, speed)

class Bullet(Square):
    def __init__(self, x_position, y_position, length = 10, speed = -15):
        super().__init__(x_position, y_position, length, length, speed)
        self.speed = speed
        self.length = length

class Powerup(Square):
    def __init__(self, x_position, y_position, width, height, speed):
        super().__init__(x_position, y_position, width, height, speed)
        self.active = False

plr = Player(screen_width/2 - 50/2, 600, 60, 60, 10)

background = pg.transform.scale((pg.image.load("pics/background.jpeg")), (screen_width, screen_height))
plr_pic = pg.transform.scale((pg.image.load("pics/ship.png")), (80, 80))
enemy_pic = pg.transform.scale((pg.image.load("pics/enemy.png")), (80, 40))
bullet_pic = pg.transform.scale((pg.image.load("pics/bullet.png")), (40, 40))
powerup_pic = pg.transform.scale((pg.image.load("pics/powerup.png")), (50, 50))
#exsplosion_pic = pg.transform.scale((pg.image.load("exsplosion.png")), (50, 50))


bullets = []
enemies = []
iterationcounter = 0
score = 0
generate_enemies = True
speed = 1
highscore = 0
powerups = []
powerup_interval = 1000
iteration = 0
enemy_spawnrate = 200
enemy_cooldown = 0
filename = "highscore.txt"


run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            
    iterationcounter += 1
    if plr.shoot_cooldown > 0:
        plr.shoot_cooldown -= 1
    
    if enemy_cooldown > 0:
        enemy_cooldown -= 1
    
    if iterationcounter % 100 == 0:
        if speed < 5:
            speed += 0.05
        if enemy_spawnrate > 50:
            enemy_spawnrate -= 10

    screen.fill((0, 0, 0))
    screen.blit(background, (0 ,0))

    font = pg.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    text_to = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    screen.blit(text_to, (10, 40))

    pos = list(plr.center())
    #pg.draw.rect(screen, (255, 0, 0), plr.rect())
    screen.blit(plr_pic, (pos[0] - 40, pos[1] - 40))

    key = pg.key.get_pressed()
    if key[pg.K_a]:
        if key[pg.K_w]:
            plr.move_to(plr.x_position - (plr.diagonal_speed), plr.y_position - plr.diagonal_speed)
        elif key[pg.K_s]:
            plr.move_to(plr.x_position - plr.diagonal_speed, plr.y_position + plr.diagonal_speed)
        else:
            plr.move_to(plr.x_position - plr.speed, plr.y_position)
    elif key[pg.K_d]:
        if key[pg.K_w]:
            plr.move_to(plr.x_position + plr.diagonal_speed, plr.y_position - plr.diagonal_speed)
        elif key[pg.K_s]:
            plr.move_to(plr.x_position + plr.diagonal_speed, plr.y_position + plr.diagonal_speed)
        else:
            plr.move_to(plr.x_position + plr.speed, plr.y_position)
    elif key[pg.K_w]:
        plr.move_to(plr.x_position, plr.y_position - plr.speed)
    elif key[pg.K_s]:
        plr.move_to(plr.x_position, plr.y_position + plr.speed)

    if key[pg.K_r]:
        plr = Player(400, 600, 50, 50, 10)
        bullets = []
        enemies = []
        powerups = []
        iterationcounter = 0
        generate_enemies = True
        score = 0
        speed = 1
        enemy_spawnrate = 200

    #generate bullets
    if key[pg.K_p]:
        plr.shoot(bullets)
        
    
    #draw and move bullets
    for bullet in bullets:
        #pg.draw.rect(screen, (255, 0, 0), bullet.rect())
        pos = list(bullet.center())
        screen.blit(bullet_pic, (pos[0] - 20, pos[1] - 20))
        bullet.move_y()
        if bullet.border_colide():
            bullets.remove(bullet)

    #generate powerups
    if iterationcounter % powerup_interval == 0:
        powerup = Powerup(random.randint(0, screen_width - 25), -50, 50, 50, 1)
        powerups.append(powerup)

    #draw and move powerups
    for powerup in powerups:
        #pg.draw.rect(screen, (200, 0, 200), powerup.rect())
        pos = list(powerup.center())
        screen.blit(powerup_pic, (pos[0] - 25, pos[1] - 25))
        powerup.move_y()
        if powerup.border_colide():
            powerups.remove(powerup)

        if powerup.rect().colliderect(plr.rect()):
            powerups.remove(powerup)
            plr.shoot_three = True
            iteration = iterationcounter

    if iterationcounter == int(iteration + 300):
        plr.shoot_three = False
       

    #generate enemies
    if generate_enemies and enemy_cooldown == 0:
        enemy = Enemy(random.randint(0, screen_width - 50), -40, 80, 40, speed)
        enemies.append(enemy)
        enemy_cooldown = enemy_spawnrate

    #draw and move enemies
    for enemy in enemies:
        pos = list(enemy.center())
        #pg.draw.rect(screen, (0, 255, 0), enemy.rect())
        screen.blit(enemy_pic, (pos[0] - 40, pos[1] - 20))
        enemy.move_y()

      
    for enemy in enemies:
        for bullet in bullets:
            if enemy.rect().colliderect(bullet.rect()):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10

                #heigscore
                if highscore <= score:
                    highscore = score
                    
                    text = str(highscore)

                    with open(filename, "w") as file:
                        file.write(text) 
                break       
        
        #heighscore
        with open(filename) as file:
            content = file.read()
            highscore = int(content)
        

        enemy_collision = enemy.rect().colliderect(plr.rect())   
        
        if enemy.border_colide() or enemy_collision:
            pg.display.update()
            pg.time.wait(1300)
            screen.fill((0, 0, 0))
            font = pg.font.Font(None, 36)
            text = font.render("Game Over", True, (255, 255, 255))
            screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
            pg.display.update()
            pg.time.wait(2000)
            screen.fill((0, 0, 0))
            textTo = font.render("Trykk på \"r\" for å starte på nytt", True, (255, 255, 255)) 
            screen.blit(textTo, (screen_width/2 - textTo.get_width()/2, screen_height/2 - textTo.get_height()/2))
            pg.display.update()

            bullets = []
            enemies = []
            powerups = []
            iterationcounter = 0
            generate_enemies = False
            score = 0
            speed = 1
            enemy_spawnrate = 200
            plr = Player(0, 0, 0, 0, 0)

            kjør = True
            while kjør:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        kjør = False
                        run = False

                key = pg.key.get_pressed()
                if key[pg.K_r]:
                    plr = Player(400, 600, 50, 50, 10)
                    generate_enemies = True
                    kjør = False
    
    pg.display.update()
    clock.tick(60)

pg.quit()