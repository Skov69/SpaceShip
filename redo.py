import pygame 
pygame.font.init()
from pygame import mixer
mixer.init()

width, height = 900, 500 
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("SPACE GAME!")


space_width, space_height = 55,40 

yellow_space = pygame.image.load("Assets/spaceship_yellow.png")
yellow_space = pygame.transform.scale(yellow_space, (space_width, space_height))
yellow_space = pygame.transform.rotate(yellow_space, 90)

red_space = pygame.image.load("Assets/spaceship_red.png")
red_space = pygame.transform.scale(red_space, (space_width, space_height))
red_space = pygame.transform.rotate(red_space, 270)

bullet_hit_sound = mixer.Sound("Assets/hit.wav")
bullet_fire_sound = mixer.Sound("Assets/shoot.wav")

border = pygame.Rect((width/2)-5, 0, 10, height)
FPS = 60
vel = 5 
bullet_vel = 10
max_bullet = 5

yellow_hit = pygame.USEREVENT + 1 
red_hit = pygame.USEREVENT + 2 

health_font = pygame.font.SysFont("Comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)

space = pygame.image.load("Pygame/Assets/space.png")
space = pygame.transform.scale(space, (width, height))

def yellow_movement(keys, yellow): 
    if keys[pygame.K_a] and yellow.x - vel > 0: #left
        yellow.x -= vel
    elif keys[pygame.K_d] and yellow.x + vel + yellow.width < border.x: #Right
        yellow.x += vel
    elif keys[pygame.K_w] and yellow.y - vel >0: #up 
        yellow.y -= vel 
    elif keys[pygame.K_s] and yellow.y + vel + yellow.height < height -15: #down 
        yellow.y += vel 



def red_movement(keys, red):
        if keys[pygame.K_LEFT] and red.x - vel > border.x + border.width: #lefts
            red.x -=  vel
        elif keys[pygame.K_RIGHT] and red.x + vel + red.width < width: #right
            red.x += vel
        elif keys[pygame.K_UP] and red.y - vel > 0: #up
            red.y -= vel
        elif keys[pygame.K_DOWN] and red.y + vel + red.height < height -15: #down
            red.y += vel
            

def handle_bullets(yellow_bullet, red_bullet, yellow, red):
    for bullet in yellow_bullet: 
        bullet.x += bullet_vel 
        if red.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullet.remove(bullet)
        elif bullet.x > width: 
            yellow_bullet.remove(bullet)

    for bullet in red_bullet: 
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullet.remove(bullet)
        elif bullet.x < 0: 
            red_bullet.remove(bullet)



def draw_winner(text): 
    draw_text = winner_font.render(text, 1, (255,255,255))
    win.blit(draw_text, (width/2 - draw_text.get_width() /2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def draw_window(yellow, red, red_bullet, yellow_bullet, red_health, yellow_health): 
    win.blit(space, (0,0))
    #win.fill((255,255,255))

    red_health_text = health_font.render("Health: " + str(red_health),1,(255,255,255))
    yellow_health_text = health_font.render("Health: " + str(yellow_health),1,(255,255,255))
    win.blit(red_health_text, (width-red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10,10))

    pygame.draw.rect(win, (0,0,0), border)
    win.blit(yellow_space, (yellow.x, yellow.y))
    win.blit(red_space, (red.x, red.y))

    for bullet in red_bullet: 
        pygame.draw.rect(win, (255,0,0), bullet)
    
    for bullet in yellow_bullet: 
        pygame.draw.rect(win, (255,0,0), bullet)

    pygame.display.update()

def main(): 

    red = pygame.Rect(700,300, space_width, space_height)
    yellow = pygame.Rect(100,300, space_width, space_height)

    yellow_bullet = []
    red_bullet = []

    red_health = 10 
    yellow_health = 10 

    clock = pygame.time.Clock()
    run = True 
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get(): # list of different events 
            if event.type == pygame.QUIT: 
                run = False 
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullet) < max_bullet:
                    bullet = pygame.Rect(yellow.x+yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullet.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and len(red_bullet) < max_bullet:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullet.append(bullet)
                    bullet_fire_sound.play()


            if event.type == red_hit:
                red_health -= 1 
                bullet_hit_sound.play()
                
            if event.type == yellow_hit:
                yellow_health -= 1 
                bullet_hit_sound.play()


        winner_text = ''
        if red_health <= 0: 
            winner_text = "Yellow wins!"

        if yellow_health <= 0: 
            winner_text = "Red wins!"

        if winner_text != "": 
            draw_winner(winner_text)
            break

        
        draw_window(yellow, red, red_bullet, yellow_bullet, red_health, yellow_health)
        keys = pygame.key.get_pressed()
        yellow_movement(keys, yellow)
        red_movement(keys, red)

        handle_bullets(yellow_bullet, red_bullet, yellow, red)
    
    



main()