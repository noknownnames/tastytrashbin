import pygame  #type: ignore
import numpy as np
import random as rand
pygame.init()

velocity=10
angle=0.5
controlcooldown=0
colliding=False
#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Textures\\taxiB.png")
        self.image = pygame.transform.scale(self.image, (50,75))
        self.rect = self.image.get_rect(center = (0.5*window_x,0.5*window_y))
        deg000=pygame.image.load("Textures\\taxiR.png")
        deg000=pygame.transform.scale(deg000, (90,75))
        deg045=pygame.image.load("Textures\\taxiBR.png")
        deg045=pygame.transform.scale(deg045, (90,75))
        deg090=pygame.image.load("Textures\\taxiB.png")
        deg090=pygame.transform.scale(deg090, (50,75))
        deg135=pygame.image.load("Textures\\taxiBL.png")
        deg135=pygame.transform.scale(deg135, (90,75))
        deg180=pygame.image.load("Textures\\taxiL.png")
        deg180=pygame.transform.scale(deg180, (90,75))
        deg225=pygame.image.load("Textures\\taxiFL.png")
        deg225=pygame.transform.scale(deg225, (90,75))
        deg270=pygame.image.load("Textures\\taxiF.png")
        deg270=pygame.transform.scale(deg270, (50,75))
        deg315=pygame.image.load("Textures\\taxiFR.png")
        deg315=pygame.transform.scale(deg315, (90,75))
        self.Rotations=[deg315,deg000,deg045,deg090,deg135,deg180,deg225,deg270]
    def texturechange(self):
        self.image = self.Rotations[int((angle//0.25+1)%8)]
    def collisiondetect(self):
        global colliding 
        if pygame.sprite.spritecollide(self,hitboxes,False):
            colliding=True
        else:
            colliding=False
    def update(self):
        self.texturechange()
        self.collisiondetect()
        

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Textures\\floor.png")
        self.image = pygame.transform.scale(self.image, (13000,13000))
        self.rect = self.image.get_rect(center = (0.5*window_x,0.5*window_y))
    def movement(self): 
            self.rect.centerx+=movex
            self.rect.centery+=movey
    def update(self):
        self.movement()

class Prop(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("Textures\\prop.png")
        self.image = pygame.transform.scale(self.image, (180,320))
        self.rect = self.image.get_rect(midbottom = (x,y))
    def movement(self):
            self.rect.centerx+=movex
            self.rect.centery+=movey
    def update(self):
        self.movement()

class Hitbox(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("Textures\\taxiB.png")
        self.image = pygame.transform.scale(self.image, (180,240))
        self.rect = self.image.get_rect(midbottom = (x,y))
    def movement(self): 
            self.rect.centerx+=movex
            self.rect.centery+=movey
    def update(self):
        self.movement()
    
#gamegeometry
window_x=1200
window_y=800
movex=0
movey=0
screen=pygame.display.set_mode((window_x,window_y))

playfield=pygame.sprite.GroupSingle()
playfield.add(Floor()) 
player=pygame.sprite.GroupSingle()
player.add(Player())

xypos=[[0*window_x,0.5*window_y]]
buildings=pygame.sprite.Group()
hitboxes=pygame.sprite.Group()
for i in range(len(xypos)):
    buildings.add(Prop(xypos[i][0],xypos[i][1]))
    hitboxes.add(Hitbox(xypos[i][0],xypos[i][1]))
while True:
    for event in pygame.event.get():
        pressed_keys=pygame.key.get_pressed()
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    #pohyb
    if controlcooldown>0:
        controlcooldown-=1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and controlcooldown==0:
        angle-=0.125
        controlcooldown=6
    if keys[pygame.K_d] and controlcooldown==0:
        angle+=0.125
        controlcooldown=6
    
    playfield.draw(screen)
    playfield.update()
    player.draw(screen)
    player.update()
    movex=np.cos(angle*np.pi)*velocity
    if colliding==True:
        movex-=np.cos(angle*np.pi)*velocity
    movey=np.sin(angle*np.pi)*velocity
    if colliding==True:
        movey=-np.cos(angle*np.pi)*velocity
    hitboxes.update()
    buildings.draw(screen)
    buildings.update()
    

    pygame.display.update()
    pygame.time.Clock().tick(60)