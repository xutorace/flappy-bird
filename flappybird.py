import pygame
import random
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
fps=60
WIDTH=864
HEIGHT=936

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
font=pygame.font.SysFont("Arial",30)

ground_scroll=0
scroll_speed=4
flying = False
game_over = False 
pipe_gap=150
pipe_frequency=1500
lastpipe=pygame.time.get_ticks()-pipe_frequency
score=0
pass_pipe=False 

bg=pygame.image.load("C:\\Users\\Hp\\Desktop\\Pro Game Development\\bg.png")
ground=pygame.image.load("ground.png")

def draw_text(text,font,text_color,x,y):
    img=font.render(text,True,text_color)
    screen.blit(img,(x,y))

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(1,4):
            img=pygame.image.load(f"flap{i}.png")
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False
        
    def update(self):
        if flying==True:
            self.vel+=0.5
            if self.vel>8:
                self.vel=8
            if self.rect.bottom<768:
                self.rect.y+=int(self.vel)
        if game_over==False:
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.vel=-10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False
                       
            self.counter+=1
            flap_cooldown=5
            if self.counter>flap_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images):
                    self.index=0
            self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pipe.png")
        self.rect=self.image.get_rect()     
        if pos==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-int(pipe_gap//2)]
        if pos==-1:
            self.rect.topleft=[x,y+int(pipe_gap//2)]
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()


bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
flappy=Bird(100,int(HEIGHT//2))
bird_group.add(flappy)


run = True
while run:
    clock.tick(fps)
    screen.blit(bg,(0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground,(ground_scroll,768))
    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right< pipe_group.sprites()[0].rect.right and pass_pipe==False:
            pass_pipe=True
        
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe=False
    draw_text(str(score),font,"red",int(WIDTH//2),30)
    
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top<0:
        game_over=True
        
    if flappy.rect.bottom>768:
        game_over=True
        flying=False

    if game_over==False and flying==True:
        time_now=pygame.time.get_ticks()

        if time_now-lastpipe>pipe_frequency:
            pipeheight=random.randint(-100,100)
            bottompipe=Pipe(WIDTH,int(HEIGHT//2)+pipeheight,-1)
            toppipe=Pipe(WIDTH,int(HEIGHT//2)+pipeheight,1)
            pipe_group.add(bottompipe)
            pipe_group.add(toppipe)
            lastpipe=time_now

        ground_scroll-=scroll_speed

        if abs(ground_scroll)>35:
            ground_scroll=0
        pipe_group.update()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False 
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True

    pygame.display.update()
