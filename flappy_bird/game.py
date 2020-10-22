import random
import sys
import time
import pygame
from pygame.locals import *

fps=32
screen_width=289
screen_height=511
screen=pygame.display.set_mode((screen_width,screen_height))
groundy=screen_height*0.8
game_image={}
game_sounds={}
bird="./gallery/images/bird.png"
background="./gallery/images/background.png"
pipe="./gallery/images/pipe.png"

def main_game():
    score=0
    playerx=int(screen_width/5)
    playery=int(screen_height/2)
    basex=0
    new_pipe1=get_random()
    new_pipe2=get_random()
    upper_pipe = [
        {'x': screen_width + 200, 'y': new_pipe1[0]['y']},
        {'x':screen_width+200+(screen_width/2),'y':new_pipe2[0]['y']}
    ]

    lower_pipe=[
        {'x': screen_width + 200, 'y': new_pipe2[1]['y']},
        {'x':screen_width+200+(screen_width/2),'y':new_pipe2[1]['y']}
    ]
    vel_x=-4
    bird_vely=-9
    bird_max=10
    bird_min=-8
    acc=1
    flappy=-8
    flapped=False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery>0:
                    bird_vely = flappy
                    flapped=True
                    game_sounds['wing'].play()

        crashed=crash(playerx,playery,upper_pipe,lower_pipe)
        if crashed:
            game_sounds["hit"].play()
            game_sounds["die"].play()
            time.sleep(2)
            screen.blit(game_image["message"], (0,0))
            pygame.display.update()
            fps_clock.tick(fps)
            time.sleep(3)
            quit()

        mid_bird=playerx+game_image['bird'].get_width()/2
        for i in upper_pipe:
            pipe_mid=i['x']+game_image['pipe'][0].get_width()/2
            if pipe_mid<=mid_bird<=pipe_mid+4:
                score=score+1
                print(f"Score: {score}")
                game_sounds["point"].play()
        if bird_vely<bird_max and not flapped:
            bird_vely=bird_vely+acc
        if flapped:
            flapped=False
        bird_height=game_image["bird"].get_height()
        playery=playery+min(bird_vely,groundy-playery-bird_height)
        for i,j in zip(upper_pipe,lower_pipe):
            i['x']=i['x']+vel_x
            j['x']=j['x']+vel_x
        if 0<upper_pipe[0]['x']<5:
            new=get_random()
            upper_pipe.append(new[0])
            lower_pipe.append(new[1])

        if upper_pipe[0]['x']<-game_image["pipe"][0].get_width():
            upper_pipe.pop(0)
            lower_pipe.pop(0)
        screen.blit(game_image["background"],(0,0))
        for i,j in zip(upper_pipe,lower_pipe):
            screen.blit(game_image["pipe"][0],(i['x'],i['y']))
            screen.blit(game_image["pipe"][1],(j['x'],j['y']))
        screen.blit(game_image["base"],(basex,groundy))
        screen.blit(game_image["bird"],(playerx,playery))
        my_digit=[int(x) for x in list(str(score))]
        width=0
        for digit in my_digit:
            width=game_image["numbers"][digit].get_width()
        off=(screen_width-width)/2
        for digit in my_digit:
            screen.blit(game_image["numbers"][digit],(off,screen_height*0.12))
            off=off+game_image["numbers"][digit].get_width()
        pygame.display.update()
        fps_clock.tick(fps)
def crash(playerx,playery,upper_pipe,lower_pipe):
    if playery>groundy-25 or playery<0:
        game_sounds["hit"].play()
        return True
    for pipes in upper_pipe:
        pipe_height=game_image["pipe"][0].get_height()
        if (playery <pipe_height + pipes['y'] and abs(playerx - pipes['x']) < game_image['pipe'][0].get_width()):
            return True
    for pipes in lower_pipe:
        pipe_height=game_image["pipe"][1].get_height()
        if (playery + game_image['bird'].get_height() > pipes['y']) and abs(playerx - pipes['x']) < game_image['pipe'][0].get_width():
            return True
    return False


def get_random():
    pipe_height=game_image["pipe"][0].get_height()
    offset=screen_height/3
    y2=offset + random.randrange(0,int(screen_height-game_image["base"].get_height()-(1.2*offset)))
    pipex=screen_width+10
    y1=pipe_height-y2+offset
    pipe=[
        {'x':pipex , 'y':-y1},
        {'x':pipex , 'y':y2}
    ]
    return pipe

if __name__ == '__main__':
    pygame.init()
    fps_clock=pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    game_image['numbers']=(
        pygame.image.load("gallery/images/0.png").convert_alpha(),
        pygame.image.load("gallery/images/1.png").convert_alpha(),
        pygame.image.load("gallery/images/2.png").convert_alpha(),
        pygame.image.load("gallery/images/3.png").convert_alpha(),
        pygame.image.load("gallery/images/4.png").convert_alpha(),
        pygame.image.load("gallery/images/5.png").convert_alpha(),
        pygame.image.load("gallery/images/6.png").convert_alpha(),
        pygame.image.load("gallery/images/7.png").convert_alpha(),
        pygame.image.load("gallery/images/8.png").convert_alpha(),
        pygame.image.load("gallery/images/9.png").convert_alpha()
    )
    game_image["message"]=pygame.image.load("gallery/images/message.jpg").convert_alpha()
    game_image["base"] = pygame.image.load("gallery/images/base.png").convert_alpha()
    game_image["background"] = pygame.image.load(background).convert_alpha()
    game_image["bird"] = pygame.image.load(bird).convert_alpha()
    game_image["pipe"] =(
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
        pygame.image.load(pipe).convert_alpha()
    )
    game_sounds["die"]=pygame.mixer.Sound("gallery/sounds/die.wav")
    game_sounds["hit"] = pygame.mixer.Sound("gallery/sounds/hit.wav")
    game_sounds["point"] = pygame.mixer.Sound("gallery/sounds/point.wav")
    game_sounds["swoosh"] = pygame.mixer.Sound("gallery/sounds/swoosh.wav")
    game_sounds["wing"] = pygame.mixer.Sound("gallery/sounds/wing.wav")

    while True:
        main_game()



