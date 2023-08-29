import pygame , sys , math , random 
from pygame.math import Vector2
pygame.init()
width = 800
height = 600
class PLAYER:
    def __init__(self):
        self.x = width/2 - 30
        self.y = 500
        self.player = pygame.image.load('C:/Users/hp/Desktop/shooter/assests/player.png').convert_alpha()
    def draw_player(self):
        player_rect = pygame.Rect(self.x,self.y,30,30)
        screen.blit(self.player,player_rect)
    def move_player(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_UP]: self.y -= 3
        if press[pygame.K_DOWN]: self.y += 3
        if press[pygame.K_RIGHT]: self.x += 3
        if press[pygame.K_LEFT]: self.x -= 3
    def collision_enemy(self):
        for check in game.enemies_list :
            if (-29<self.x - check.x<29) and (-29<self.y - check.y<29):
                return True
        return False
class BULLET:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 10
        # Calculate direction
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
    def draw(self):
        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), 5)

class ENEMY:
    
    def __init__(self):
        self.direction_x = Vector2(0.7,0)
        self.direction_y = Vector2(0,0.7)
        self.enemy_image=pygame.image.load('C:/Users/hp/Desktop/shooter/assests/virus.png').convert_alpha()
        self.sound_effect = pygame.mixer.Sound('C:/Users/hp/Desktop/shooter/sounds/Laser.mp3')
        self.sound_effect.set_volume(0.3)

    def draw_enemy(self):
        for enemy in game.enemies_list:
            enemy_rect = pygame.Rect(enemy.x,enemy.y,30,30)
            screen.blit(self.enemy_image,enemy_rect)
    
    def move_enemy(self):
        global enemies_list
        for index,enemy in enumerate(game.enemies_list):
            if enemy.x < game.player.x and enemy.y < game.player.y:
                enemy.x += self.direction_x.x
                enemy.y += self.direction_y.y
            if enemy.x < game.player.x and enemy.y > game.player.y:
                enemy.x += self.direction_x.x
                enemy.y -= self.direction_y.y
            if enemy.x > game.player.x and enemy.y < game.player.y:
                enemy.x -= self.direction_x.x
                enemy.y += self.direction_y.y
            if enemy.x > game.player.x and enemy.y > game.player.y:
                enemy.x -= self.direction_x.x
                enemy.y -= self.direction_y.y
            if enemy.x < game.player.x : enemy.x += self.direction_x.x
            if enemy.x > game.player.x : enemy.x -= self.direction_x.x
            if enemy.y > game.player.y : enemy.y += self.direction_y.y
            if enemy.y > game.player.y : enemy.y -= self.direction_y.y
            body_copy = game.enemies_list
            body_copy.insert(index,enemy)
            body_copy.remove(body_copy[index+1])
        game.enemies_list = body_copy
         
    def collision_bullet(self):
        global test,score
        num=len(game.bullets)
        if num>=1 :
            last= game.bullets[num-1]
            for check in game.enemies_list :
                if (-29<=(check.x - last.x)+ 30 <= 30) and (-29<=(check.y - last.y)+ 30 <= 30):
                    game.test = True
                    game.enemies_list.remove(check)
                    game.enemy.randomize()
                    game.score += 1
                    self.sound_effect.play()

                    
    def randomize(self):
        self.x = random.randint(-100,900)
        self.y = random.randint(-100,700)
        game.enemies_list.append(Vector2(self.x,self.y))
        
    def calculate_score(self): 
        score_x =700
        score_y = 550
        score_text = 'score : '+str(game.score)
        score_surface = game.game_font.render(score_text,True,(255,255,255))
        score_rect=  score_surface.get_rect(center=(score_x,score_y))
        screen.blit(score_surface,score_rect)
class GAME:
    def __init__(self):
        self.player = PLAYER()
        self.enemy = ENEMY()
        self.game_state = 'start'  # Can be 'start', 'playing', or 'game_over'
        self.score = 0
        self.test = False
        self.bullets = []
        self.enemies_list = [ Vector2(0,0) ]
        self.game_font = pygame.font.Font(None,25)
    def draw(self):
        self.player.draw_player()
        self. enemy.draw_enemy()
        for bullet in game.bullets:
                bullet.update()
                bullet.draw()
        if game.test:
            game.bullets.clear()
            game.enemy.randomize()
            game.test = False
    def move(self):
        self.player.move_player()
        self.enemy.move_enemy()
        
    def start_menu(self):
        screen.blit(bg, bg_rect)
        self.title_font = pygame.font.Font(None, 50)
        self.title = self.title_font.render('Shooter Game', True, (255, 255, 255))
        title_rect = self.title.get_rect(center=(width / 2, height / 2 - 100))
        screen.blit(self.title, title_rect)

        play_button = pygame.Rect(width / 2 - 70, height / 2, 140, 50)
        self.play_text = game.game_font.render('Play', True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), play_button)
        screen.blit(self.play_text, play_button.move(40, 10))

        return play_button


    def game_over_menu(self):
    
        screen.blit(bg, bg_rect)
        self.game_over_font = pygame.font.Font(None, 50)
        self.game_over_text = self.game_over_font.render('Game Over', True, (255, 255, 255))
        game_over_rect = self.game_over_text.get_rect(center=(width / 2, height / 2 - 100))
        screen.blit(self.game_over_text, game_over_rect)
    
        self.score_text = 'score : '+str(game.score)
        self.score_surface = self.game_over_font.render(self.score_text,True,(255,255,255))
        score_rect=  self.score_surface.get_rect(center=(width / 2, height / 2 - 60))
        screen.blit(self.score_surface,score_rect)

        replay_button = pygame.Rect(width / 2 - 70, height / 2, 140, 50)
        self.replay_text = game.game_font.render('Replay', True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), replay_button)
        screen.blit(self.replay_text, replay_button.move(30, 10))
        return replay_button

    def reset_game(self):
    
        game.bullets = []
        game.enemies_list = [Vector2(0, 0)]
        game.score = 0
        game.test = False
        game.player = PLAYER()
        game.enemy = ENEMY()


screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('shooter game')
bg=pygame.image.load('C:/Users/hp/Desktop/shooter/assests/bg.png').convert_alpha()
bg=pygame.transform.scale2x(bg)
bg_rect=bg.get_rect(center=(width/2,height/2))

clock=pygame.time.Clock()
game = GAME()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game.game_state == 'start' and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if game.start_menu().collidepoint(x, y):
                game.game_state = 'playing'
        if game.game_state == 'game_over' and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if game.game_over_menu().collidepoint(x, y):
                game.reset_game()  # Reset the game state and necessary game variables
                game.game_state = 'playing'
        if game.game_state == 'playing' and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            game.bullets.append(BULLET(game.player.x + 30 // 2, game.player.y + 30 // 2, x, y))
    # Draw and update according to game state
    if game.game_state == 'start':
        game.start_menu()
    elif game.game_state == 'playing':
        screen.blit(bg, bg_rect)
        if game.player.collision_enemy():
            game.game_state = 'game_over'
            continue  # Skip the rest of this iteration to instantly show game over     
        game.move()
        game.enemy.collision_bullet()
        game.draw()
        game.enemy.calculate_score()
    elif game.game_state == 'game_over':
        game.game_over_menu()
    pygame.display.update()
    clock.tick(60)

