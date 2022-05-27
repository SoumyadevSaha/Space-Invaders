import pygame
import random

pygame.init()

# Space Ships ->
MY_SHIP = pygame.image.load("Assets\\Images\\player.png")
ENEMY_1 = pygame.image.load("Assets\\Images\\enemy1.png")
ENEMY_2 = pygame.image.load("Assets\\Images\\enemy2.png")
ENEMY_3 = pygame.image.load("Assets\\Images\\enemy3.png")

# Lasers ->
LASER_1 = pygame.image.load("Assets\\Images\\laser1.png")
LASER_2 = pygame.image.load("Assets\\Images\\laser2.png")
BLAST = pygame.image.load("Assets\\Images\\blast.png")

# FORCE FIELD ->
FORCE_FIELD = pygame.image.load("Assets\\Images\\force_field.png")
CHEAT_CODE = "ch69"

# Game Music and Sounds ->
SHOOT = pygame.mixer.Sound("Assets\\Music\\shoot.wav")
# LEVEL_UP = pygame.mixer.Sound("levelup.wav")
pygame.mixer.music.load("Assets\\Music\\gameBGM.mp3")
pygame.mixer.music.play(-1)

# Pygame Fonts ->
FONT = pygame.font.SysFont("comicsans", 25)

# Game Screen ->
WIDTH, HEIGHT = 1200, 800
BACKGROND = pygame.image.load("Assets\\Images\\background.jpg")
BG = pygame.transform.scale(BACKGROND, (WIDTH, HEIGHT))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders | By : Soumyadev")

# Main Ship Class ->
class Ship:
    def __init__(self, x, y, id=None):
        self.x = x
        self.y = y
        self.id = id
        self.img = None
        self.laser_img = None
        self.lasers = []
        self.dead = False
        self.coolDown = 0
    def draw(self) :
        rect = self.img.get_rect()
        rect.center = (self.x, self.y)
        WIN.blit(self.img, rect)
        for laser in self.lasers:
            WIN.blit(self.laser_img, laser)
            if laser[1] < 0 or laser[1] > HEIGHT:
                self.lasers.remove(laser)
        # Drawing the health bar ->
        if not self.id :
            healthPt = (rect.centerx - self.img.get_width() / 2, rect.centery + 15 + self.img.get_height() / 2)
        else :
            healthPt = (rect.centerx - self.img.get_width() / 2, rect.centery - 50 + self.img.get_height() / 2)
        green = (self.health / self.thealth) * self.img.get_width()
        pygame.draw.rect(WIN, (0, 255, 0), (healthPt[0], healthPt[1], green, 5))
        red = ((self.thealth - self.health) / self.thealth)*self.img.get_width()
        pygame.draw.rect(WIN, (255, 0, 0), (healthPt[0] + green, healthPt[1], red, 5))

    def shoot(self) :
        if self.coolDown :
            self.coolDown -= 1

    def takeDamage(self) :
        self.health -= 10
        if self.health <= 0:
            self.dead = True

# Class for the player ship ->
class MyShip(Ship) :
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = MY_SHIP
        self.laser_img = LASER_1
        self.thealth = 200
        self.health = self.thealth
    def draw(self):
        super().draw()
        for laser in self.lasers:
            laser[1] -= 10
    def shoot(self):
        super().shoot()
        if (not self.dead) and (self.coolDown == 0):
            self.lasers.append([self.x + 7, self.y - self.img.get_height() / 2])
            self.lasers.append([self.x - 65, self.y - self.img.get_height() / 2])

class EnemyShip(Ship) :
    def __init__(self, x, y, id) :
        super().__init__(x, y, id)
        if id == 1 :
            self.img = ENEMY_1
            self.thealth = 10
        elif id == 2 :
            self.img = ENEMY_2
            self.thealth = 20
        elif id == 3 :
            self.img = ENEMY_3
            self.thealth = 40
        self.health = self.thealth
        self.laser_img = LASER_2
        self.coolDown = 300 // self.id
    def draw(self):
        super().draw()
        for laser in self.lasers:
            laser[1] += 10
    def shoot(self):
        super().shoot()
        if (not self.dead) and (self.coolDown == 0):
            self.lasers.append([self.x - 30, self.y - 14])
            self.coolDown = 300 // self.id

# Drawing on the Game screen ->
def draw_screen(my_ship, lives, score, level, enemies, gameOver, shield) :
    WIN.blit(BG, (0, 0))

    # Drawing the Player ->
    my_ship.draw()
    if shield :
        WIN.blit(FORCE_FIELD, (my_ship.x - FORCE_FIELD.get_width() / 2, my_ship.y - 80 - FORCE_FIELD.get_height() / 2))

    # Drawing the Enemies ->
    for enemy in enemies :
        if not gameOver :
            enemy.shoot()
        enemy.draw()

    # Drawing the Lives, score and level ->
    label1 = FONT.render("Lives : " + str(lives), 1, (255, 255, 255))
    label2 = FONT.render("Score : " + str(score), 1, (255, 255, 255))
    label3 = FONT.render("Level : " + str(level), 1, (255, 255, 255))
    WIN.blit(label1, (20, 10))
    WIN.blit(label2, (WIDTH // 2 - label2.get_width()//2, 10))
    WIN.blit(label3, (WIDTH - label3.get_width() - 20, 10))

    if gameOver :
        FONT2 = pygame.font.SysFont("comicsans", 100)
        label = FONT2.render("Game Over !!!", 1, (255, 0, 0))
        WIN.blit(label, (WIDTH // 2 - label.get_width()//2, HEIGHT // 2 - label.get_height()//4))
    if my_ship.dead :
        b_rect = BLAST.get_rect()
        b_rect.center = (my_ship.x, my_ship.y + 15)
        WIN.blit(BLAST, b_rect)

    pygame.display.update()

# Main Function ->
def main() :
    run = True
    fps = 60
    clock = pygame.time.Clock()
    pressed = ""
    level = 0
    score = 0
    lives = 7
    gameOver, played = False, False
    shield = 0
    cheat = ""

    # Initializing the Player ->
    my_ship = MyShip(WIDTH // 2, HEIGHT - 100)

    # Enemy Ships ->
    enemy_ships = []

    # Game Loop ->
    while run :
        clock.tick(fps)

        # Handling Events ->
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.KEYDOWN :
                # Handling Shooting event ->
                if event.key == pygame.K_SPACE :
                    if not gameOver :
                        SHOOT.play()
                    my_ship.shoot()
                if not my_ship.dead :
                # Handling Movement event ->
                    if event.key == pygame.K_LEFT and my_ship.x > 50 :
                        my_ship.x += 5
                        pressed = "left"
                    if event.key == pygame.K_RIGHT and my_ship.x < WIDTH - 50 :
                        my_ship.x -= 5
                        pressed = "right"
                    if event.key == pygame.K_UP and my_ship.y > 50 :
                        my_ship.y += 5
                        pressed = "up"
                    if event.key == pygame.K_DOWN and my_ship.y < HEIGHT - 50 :
                        my_ship.y -= 5
                        pressed = "down"
                # Handling cheat code ->
                if not shield :
                    if event.key == pygame.K_c :
                        cheat += "c"
                    elif event.key == pygame.K_h :
                        cheat += "h"
                    elif event.key == pygame.K_6 :
                        cheat += "6"
                    elif event.key == pygame.K_9 :
                        cheat += "9"
                    else :
                        cheat = ""
            if event.type == pygame.KEYUP :
                pressed = ""

        # Handling continuious key press ->
        if pressed :
            if pressed == "left" and my_ship.x > 50 :
                my_ship.x -= 5
            if pressed == "right" and my_ship.x < WIDTH - 50 :
                my_ship.x += 5
            if pressed == "up" and my_ship.y > 50 :
                my_ship.y -= 5
            if pressed == "down" and my_ship.y < HEIGHT - 50 :
                my_ship.y += 5

        # Handling cheat code ->
        if cheat == CHEAT_CODE :
            shield = 15
            cheat = ""
        
        # Game Logic ->
        if len(enemy_ships) == 0 :
            level += 1
            for _ in range((level * 3) // 2) :
                x = random.randint(50, WIDTH - 50)
                y = random.randint(-500, 0)
                if level <= 5 :
                    enemy_ships.append(EnemyShip(x, y, 1))
                elif level <= 10 and level > 5 :
                    ship_id = random.randint(1, 2)
                    enemy_ships.append(EnemyShip(x, y, ship_id))
                else :
                    ship_id = random.randint(1, 3)
                    enemy_ships.append(EnemyShip(x, y, ship_id))

        for enemy in enemy_ships :
            if enemy.dead :
                score += 10*enemy.id
                enemy_ships.remove(enemy)
            elif enemy.y > HEIGHT - 50 :
                enemy_ships.remove(enemy)
                lives -= 1
            else :
                if not gameOver :
                    enemy.y += 0.5

        # Handling cheat force shield ->
        if shield :
            for enemy in enemy_ships :
                for laser in enemy.lasers :
                    # shield_rect = FORCE_FIELD.get_rect()
                    if laser[1] + 160 > my_ship.y - FORCE_FIELD.get_height() // 2 and laser[1] + 160 < my_ship.y + FORCE_FIELD.get_height() // 2 :
                        if laser[0] + 30 > my_ship.x - FORCE_FIELD.get_width() // 2 and laser[0] + 30 < my_ship.x + FORCE_FIELD.get_width() // 2 :
                            enemy.lasers.remove(laser)
                            shield -= 1
        # My Ship takes damage
        if not shield :
            for enemy in enemy_ships :
                for laser in enemy.lasers :
                    if laser[1] + 80 > my_ship.y - my_ship.img.get_height() // 2 and laser[1] + 80 < my_ship.y + my_ship.img.get_height() // 2 :
                        if laser[0] + 30 > my_ship.x - my_ship.img.get_width() // 2 and laser[0] + 30 < my_ship.x + my_ship.img.get_width() // 2 :
                            enemy.lasers.remove(laser)
                            my_ship.takeDamage() 
        # Enemy takes damage
        for enemy in enemy_ships :
            for laser in my_ship.lasers :
                if laser[1] + 30 > enemy.y - enemy.img.get_height()//2 and laser[1] + 30 < enemy.y + enemy.img.get_height()//2 :
                    if laser[0] + 30 > enemy.x - enemy.img.get_width()//2 and laser[0] + 30 < enemy.x + enemy.img.get_width()//2 :
                        # enemy.lasers.remove(laser)
                        my_ship.lasers.remove(laser)
                        enemy.takeDamage()
 
        # Drawing on Screen ->
        draw_screen(my_ship, lives, score, level, enemy_ships, gameOver, shield) 

        # Handling gameOver music ->
        if (my_ship.dead or lives <= 0) and not played:
            gameOver = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Assets\\Music\\gameOver.wav")
            pygame.mixer.music.play()
            played = True

    pygame.quit()

if __name__ == "__main__" :
    main()