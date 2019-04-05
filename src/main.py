import upygame as upg
import umachine
import sprites
import titlescreen
import sfx

from levels import *
from urandom import getrandbits as rnd


version="v1.1"

upg.display.init(True)
screen = upg.display.set_mode() # full screen

# Initialize sound
g_sound = upg.mixer.Sound()

upg.display.set_palette_16bit([
    0x0000, 0xffff, 0xf81f, 0x07ff,
    0xffe2, 0x67ed, 0x001f, 0xf800,
    0x5aeb, 0x9cd3, 0x780f, 0x4471,
    0x82e5, 0x03e7, 0x0013, 0xa800,
    ]);

def sign(a):
    return (a > 0) - (a < 0)

# globales

tiles=[0,sprites.ladder8,0,0,
sprites.coin8,sprites.emerald8,0,sprites.bricks8,
sprites.fuel_big8,sprites.cobblestone8,0,0,
0,sprites.emeraldEmpty8,0,0]

player_right=[sprites.player8_1,sprites.player8_2,sprites.player8_3]
player_left=[sprites.player8_1l,sprites.player8_2l,sprites.player8_3l]
player_death=[sprites.playerDead8_1,sprites.playerDead8_2,sprites.playerDead8_3,sprites.playerDead8_4]
flame=[sprites.flame1,sprites.flame2,sprites.flame3]

solids=[7,9]

scrwidth=110
scrheight=88-8

camerax=0
cameray=0

spritesize=8

frame=0
score=0
extralives=0

# 0=Left 1=Right 2=Up 3=Down 4=A 5=B 6=C

btns = [False,False,False,False,False,False,False]



def poll_btns():
    eventtype = upg.event.poll()
    if eventtype != upg.NOEVENT:
        if eventtype.type == upg.KEYDOWN:
            if eventtype.key == upg.K_LEFT:  btns[0]=True
            if eventtype.key == upg.K_RIGHT: btns[1]=True
            if eventtype.key == upg.K_UP:    btns[2]=True
            if eventtype.key == upg.K_DOWN:  btns[3]=True
            if eventtype.key == upg.BUT_A :  btns[4]=True
            if eventtype.key == upg.BUT_B :  btns[5]=True
            if eventtype.key == upg.BUT_C :  btns[6]=True
        if eventtype.type == upg.KEYUP:
            if eventtype.key == upg.K_LEFT:  btns[0]=False
            if eventtype.key == upg.K_RIGHT: btns[1]=False
            if eventtype.key == upg.K_UP:    btns[2]=False
            if eventtype.key == upg.K_DOWN:  btns[3]=False
            if eventtype.key == upg.BUT_A :  btns[4]=False
            if eventtype.key == upg.BUT_B :  btns[5]=False
            if eventtype.key == upg.BUT_C :  btns[6]=False

class Trackbot:
    def __init__(self,x,y):
        self.w = spritesize
        self.h = spritesize
        self.x = x
        self.y = y
        self.dx = 1
        self.t = 0
        
    def update(self):
        if self.t>0:
            self.t -= 1
        else:
            self.x += self.dx
        
        if self.dx < 0 and not level.solid_at(self.x,self.y+self.h+4) and not level.ladder_at(self.x,self.y+self.h+4):
            self.dx = -self.dx
            self.t=20
        if self.dx > 0 and not level.solid_at(self.x+self.w,self.y+self.h+4) and not level.ladder_at(self.x+self.w,self.y+self.h+4):
            self.dx = -self.dx
            self.t=20
            
        if self.dx < 0 and level.solid_at(self.x-1,self.y) :
            self.dx = -self.dx
            self.t=20
        if self.dx > 0 and level.solid_at(self.x+self.w+1,self.y) :
            self.dx = -self.dx
            self.t=20
            
        if self.dx < 0 and self.x < 0:
            self.dx = -self.dx
            self.t=20
        if self.dx > 0 and self.x+self.w > level.w :
            self.dx = -self.dx
            self.t=20
        
        
    def draw(self):
        if self.x%4 <2 :
            screen.blit(sprites.bot8_1, self.x-camerax, self.y-cameray)
        else:
            screen.blit(sprites.bot8_2, self.x-camerax, self.y-cameray)
        

class Steelball:
    def __init__(self,x,y):
        self.w = spritesize
        self.h = spritesize
        self.x = x
        self.y = y
        self.dx = 2

        
    def update(self):
        
        self.x += self.dx
        
        if self.dx < 0 and not level.solid_at(self.x,self.y+self.h+4) and not level.ladder_at(self.x,self.y+self.h+4):
            self.dx = -self.dx

        if self.dx > 0 and not level.solid_at(self.x+self.w,self.y+self.h+4) and not level.ladder_at(self.x+self.w,self.y+self.h+4):
            self.dx = -self.dx

            
        if self.dx < 0 and level.solid_at(self.x-1,self.y) :
            self.dx = -self.dx

        if self.dx > 0 and level.solid_at(self.x+self.w+1,self.y) :
            self.dx = -self.dx
            
        if self.dx < 0 and self.x < 0:
            self.dx = -self.dx
            
        if self.dx > 0 and self.x+self.w > level.w :
            self.dx = -self.dx
            

        
        
    def draw(self):
        screen.blit(sprites.sball8, self.x-camerax, self.y-cameray)


class Spring:
    def __init__(self,x,y):
        self.w = spritesize
        self.h = spritesize
        self.x = x
        self.y = y
        self.dy = 2

        
    def update(self):
        
        self.y += self.dy
            
        if self.dy < 0 and level.solid_at(self.x,self.y) :
            self.dy = -self.dy

        if self.dy > 0 and level.solid_at(self.x,self.y+self.h) :
            self.dy = -self.dy
            
        if self.dy < 0 and self.y < 0 :
            self.dy = -self.dy

        if self.dy > 0 and self.y+self.h > level.h :
            self.dy = -self.dy
        
    def draw(self):
        
        if self.y%8 < 4:
            screen.blit(sprites.spring8_1, self.x-camerax, self.y-cameray)
        else:
            screen.blit(sprites.spring8_2, self.x-camerax, self.y-cameray)       
        
        
class Missile:
    def __init__(self,x,y):
        self.w = spritesize
        self.h = spritesize
        self.x = x
        self.y = y
        self.dx = -2
        self.dy = 0

        
    def update(self):
        
        self.y += self.dy
        self.x += self.dx
            
        if self.dy < 0 and (level.solid_at(self.x+3,self.y-1) or self.y < 0):
            self.dx = self.dy
            self.dy=0
            return

        if self.dy > 0 and (level.solid_at(self.x+3,self.y+self.h+1) or self.y+self.h > level.h) :
            self.dx = self.dy
            self.dy=0
            return
            
        if self.dx < 0 and (level.solid_at(self.x-1,self.y+3) or self.x <0):
            self.dy = -self.dx
            self.dx=0
            return

        if self.dx > 0 and (level.solid_at(self.x+self.w+1,self.y+3) or self.x+self.w > level.w):
            self.dy = -self.dx
            self.dx=0
            return
            

    def draw(self):
        
        if self.dy > 0:
            screen.blit(sprites.missile8_Down, self.x-camerax, self.y-cameray)
        if self.dy < 0:
            screen.blit(sprites.missile8_Up, self.x-camerax, self.y-cameray)
        if self.dx > 0:
            screen.blit(sprites.missile8_Right, self.x-camerax, self.y-cameray)
        if self.dx < 0:
            screen.blit(sprites.missile8_Left, self.x-camerax, self.y-cameray)
   
   
class Spike:
    def __init__(self,x,y):
        self.w = spritesize//2
        self.h = spritesize//2
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1

        
    def update(self):
        
        self.y += self.dy
        self.x += self.dx
            
        if self.dy < 0 and (level.solid_at(self.x+1,self.y-1) or self.y < 0):
            self.dy = -self.dy
            return

        if self.dy > 0 and (level.solid_at(self.x+1,self.y+self.h+1) or self.y +self.h >level.h):
            self.dy = -self.dy
            return
            
        if self.dx < 0 and (level.solid_at(self.x-1,self.y+1) or self.x < 0) :
            self.dx = -self.dx
            return

        if self.dx > 0 and (level.solid_at(self.x+self.w+1,self.y+1) or self.x+self.w >level.w):
            self.dx = -self.dx
            return
            

    def draw(self):
        
        if frame%4==0:
            screen.blit(sprites.spikes8_1, self.x-camerax, self.y-cameray)
        if frame%4==1:
            screen.blit(sprites.spikes8_2, self.x-camerax, self.y-cameray)
        if frame%4==2:
            screen.blit(sprites.spikes8_3, self.x-camerax, self.y-cameray)
        if frame%4==3:
            screen.blit(sprites.spikes8_4, self.x-camerax, self.y-cameray)        
    

class Level:
    def __init__(self):
        self.w=0
        self.h=0
        self.map=0
        self.emeralds=0
        self.lvl_nmbr=0
        self.load(levels[self.lvl_nmbr])
        self.newlvl=True
        self.t_new=30

        
    def next(self):
        
        self.lvl_nmbr +=1
        if self.lvl_nmbr >= len(levels):
            global win
            global gameover
            global t_gameover
            
            win=True
            gameover=True
            t_gameover=300
            return
        
        self.load(levels[self.lvl_nmbr])
        
    def load(self,lvl):
        self.w=lvl[0]*spritesize
        self.h=lvl[1]*spritesize
        self.data=lvl[2]
        
        
        
        self.reload()
                
    def reload(self):
        
        self.newlvl=True
        self.t_new=30
        
        self.map=bytearray(self.data)
        global bots
        global balls
        global springs
        global missiles
        global spikes
        
        bots=[]
        balls=[]
        springs=[]
        spikes=[]
        missiles=[]
        self.emeralds=0
        
        wid=(self.w//spritesize)//2
        for j in range(0,self.h//spritesize):
            for i in range(0,(self.w//spritesize)//2):
                c1=self.map[j*wid+i]>>4
                c2=self.map[j*wid+i]&0xf
                
                global p1
                
                if c1 == 2:
                    p1.x=i*2*spritesize
                    p1.y=j*spritesize

                if c2 == 2:
                    p1.x=(1+i*2)*spritesize
                    p1.y=j*spritesize
                    
                

                if c1 == 5:
                    self.emeralds+=1
                if c2 == 5:
                    self.emeralds+=1
                
                #trackbot    
                if c1 == 0xa:
                    bots.append(Trackbot(i*2*spritesize,j*spritesize))
                if c2 == 0xa:
                    bots.append(Trackbot((1+i*2)*spritesize,j*spritesize))
                #steelball    
                if c1 == 3:
                    balls.append(Steelball(i*2*spritesize,j*spritesize))
                if c2 == 3:
                    balls.append(Steelball((1+i*2)*spritesize,j*spritesize))
                    
                #springs
                if c1 == 0xe:
                    springs.append(Spring(i*2*spritesize,j*spritesize))
                if c2 == 0xe:
                    springs.append(Spring((1+i*2)*spritesize,j*spritesize))
                    
                #missils
                if c1 == 0x6:
                    missiles.append(Missile(i*2*spritesize,j*spritesize))
                if c2 == 0x6:
                    missiles.append(Missile((1+i*2)*spritesize,j*spritesize))
                    
                #spikes
                if c1 == 0xf:
                    spikes.append(Spike(i*2*spritesize,j*spritesize))
                if c2 == 0xf:
                    spikes.append(Spike((1+i*2)*spritesize,j*spritesize))
                    
                i+=1
        
    def tile_at(self,x,y):
        if x <0 or y < 0 or x > self.w or y > self.h:
            return 7
        
        tile_x=x//spritesize
        tile_y=y//spritesize
        
        d=self.map[tile_y*(self.w//spritesize)//2+tile_x//2]
        if tile_x % 2 : return d&0xf
        else: return d>>4
        
    def set_tile(self,x,y,value):
        tile_x=x//spritesize
        tile_y=y//spritesize
        d=self.map[tile_y*(self.w//spritesize)//2+tile_x//2]
        if tile_x % 2 ==0 :
            self.map[tile_y*(self.w//spritesize)//2+tile_x//2]=((d&0x0f) | (value<<4))
        else:
            self.map[tile_y*(self.w//spritesize)//2+tile_x//2]=((d&0xf0) | value)
        
    def solid_at(self,x,y):
        t=self.tile_at(x,y)
        for s in solids:
            if t== s:
                return True
        return False   
         
    def ladder_at(self,x,y):
        t=self.tile_at(x,y)
        if t== 1:
            return True
        else:
            return False
            
    def collisionAtPosition(self,tile,xc, yc, wc, hc):
        if self.tile_at(xc, yc + hc-1) == tile:
            return True
        if self.tile_at(xc + wc-1, yc + hc-1) == tile:
            return True
        if self.tile_at(xc + wc-1, yc) == tile:
            return True
        if self.tile_at(xc, yc) == tile:
            return True
            
    def solidCollisionAtPosition(self,xc, yc, wc, hc):
        if self.solid_at(xc, yc + hc-1):
            return True
        if self.solid_at(xc + wc-1, yc + hc-1):
            return True
        if self.solid_at(xc + wc-1, yc):
            return True
        if self.solid_at(xc, yc):
            return True

            
    def draw(self):
        xmin=camerax//spritesize
        xmax=(scrwidth//spritesize+camerax//spritesize)+2
        
        ymin=cameray//spritesize
        ymax=(scrheight//spritesize+cameray//spritesize)+2
        wid=(self.w//2)//spritesize
        doordraw=False
        for j in range(ymin,ymax):
            for i in range((xmin-1)//2,(xmax+1)//2):
                if i<0 or j < 0 or i >= wid or j >= self.h//spritesize:
                    continue
                
                c1=self.map[j*wid+i]>>4
                c2=self.map[j*wid+i]&0xf
                if not c1==0 and not tiles[c1] == 0:
                    screen.blit(tiles[c1], i*2*spritesize-camerax,j*spritesize -cameray, 16)
                if not c2==0 and not tiles[c2] == 0:
                    screen.blit(tiles[c2], i*2*spritesize-camerax+spritesize,j*spritesize -cameray, 16)
                    
                if c1==0xb:
                    if not self.solid_at(i*2*spritesize,(j-1)*spritesize):
                        screen.blit(sprites.spikesDown8, i*2*spritesize-camerax,j*spritesize -cameray, 16)
                    else:
                        screen.blit(sprites.spikesUp8, i*2*spritesize-camerax,j*spritesize -cameray, 16)
                        
                if c2==0xb:
                    if not self.solid_at(i*2*spritesize+spritesize,(j-1)*spritesize):
                        screen.blit(sprites.spikesDown8, i*2*spritesize-camerax+spritesize,j*spritesize -cameray, 16)
                    else:
                        screen.blit(sprites.spikesUp8, i*2*spritesize-camerax+spritesize,j*spritesize -cameray, 16)
                    
                if c1==0xc and not doordraw:
                    doordraw=True
                    if self.emeralds== p1.emeralds:
                        screen.blit(sprites.doorOpened, i*2*spritesize-camerax,j*spritesize -cameray, 16)
                    else:
                        screen.blit(sprites.doorClosed, i*2*spritesize-camerax,j*spritesize -cameray, 16)
                if c2==0xc and not doordraw:
                    doordraw=True
                    if self.emeralds== p1.emeralds:
                        screen.blit(sprites.doorOpened, i*2*spritesize-camerax+spritesize,j*spritesize -cameray, 16)
                    else:
                        screen.blit(sprites.doorClosed, i*2*spritesize-camerax+spritesize,j*spritesize -cameray, 16)
                i=i+1
        
      


class Player:
    def __init__(self,x,y):
        self.vx=0
        self.vy=0
        self.x=x
        self.y=y
        self.h=spritesize
        self.w=6
        self.dir=1
        self.gravity=1
        self.climb=False
        self.walk=False
        self.gnd=False
        self.jp=0
        self.fuel=0
        self.jpmax=3
        self.f=0
        self.lives=4
        self.emeralds=0
        self.dead = False
        
    def updatecamera(self):
        global camerax
        global cameray
        camerax=(self.x+self.w//2) - scrwidth//2
        if camerax < 0 :
            camerax=0;
        if camerax > level.w - scrwidth:
            camerax=level.w - scrwidth
            
        cameray=(self.y+self.h//2) - scrheight//2
        if cameray < 0 :
            cameray=0;
        if cameray > level.h - scrheight:
            cameray=level.h - scrheight
     
    def enemiesCollision(self):
     
        for bot in bots:
            if abs(bot.x+4-self.x) < 4 and abs(bot.y-self.y) < 7:
                return True
        for ball in balls:
            if abs(ball.x+2-self.x) < 4 and abs(ball.y+2-self.y) < 4:
                return True
        for spr in springs:
            if abs(spr.x+2-self.x) < 4 and abs(spr.y+2-self.y) < 4:
                return True
        for msl in missiles:
            if abs(msl.x+3-self.x) < 4 and abs(msl.y+3-self.y) < 4:
                return True
        for spk in spikes:
            if abs(spk.x+2-self.x) < 4 and abs(spk.y+2-self.y) < 4:
                return True
            
        return False
            
    def update(self):
        global frame
        global extralives
        global score
        
        if score//10000 > extralives:
            extralives +=1
            self.lives +=1
            
        if self.dead:
            if frame%6==5:
                self.f +=1
            if self.f>3:
                if self.lives < 0:
                    global gameover
                    global t_gameover
                    gameover=True
                    t_gameover=100
                    return
                
                level.reload()
                self.vx=0
                self.vy=0
                self.dir=1
                self.climb=False
                self.walk=False
                self.jp=0
                self.fuel=0
                self.f=0
                self.emeralds=0
                self.dead = False
            return
        
        oy=self.y
    
        #climb
        self.climb=False
        self.w=6
        if level.ladder_at(self.x+2,self.y+self.h) or level.ladder_at(self.x+2,self.y+self.h//2) :
            self.climb=True
            self.w=4
            if level.ladder_at(self.x+2,self.y+self.h) and not level.ladder_at(self.x+2,self.y+7):
                self.climb=False
                self.vy=0
                
            if btns[2] and self.climb:
                self.vy =-2 #up
            if btns[3] :
                self.vy =2 #down
            if not btns[2] and not btns[3]:
                self.vy =0
        else:
            self.vy += self.gravity
                
        if btns[4] and self.fuel > 0:
            g_sound.play_sfx(sfx.jetpack, len(sfx.jetpack), True)
            self.jp += 2
            if self.jp > self.jpmax:
                self.jp = self.jpmax
            self.fuel-=1
            
        if self.jp > 0:
            if self.gnd:
                self.vy=0
            self.vy -= self.jp
            self.jp -= 1
            
        if self.vy > self.jpmax:
            self.vy = self.jpmax
        if self.vy < -self.jpmax:
            self.vy = -self.jpmax
                
        #left/right
        
        if btns[0]:
            self.vx =-2 #Left
            self.walk=True
            self.dir=-1
        
        if btns[1]:
            self.vx = 2 #Right
            self.walk=True
            self.dir=1
            
        if not btns[0] and not btns[1]:
            self.vx =0
            self.walk=False
            
            
        if btns[6]: #C button restart the level
            self.dead=True
            self.f=0
        
        if(self.x<0): self.x=0
        if(self.x+self.w  > level.w ): self.x = level.w-self.w
        
        if not level.solidCollisionAtPosition(self.x+self.vx,self.y,self.w,self.h):
            self.x += self.vx
        
        
        if(self.y<0): self.y=0
        if(self.y+self.h  > level.h ): self.y = level.h -self.h
        
        
        if not level.solidCollisionAtPosition(self.x,self.y+self.vy//2,self.w,self.h):
            self.y += self.vy//2
        
        else:
            if not level.solidCollisionAtPosition(self.x,self.y+sign(self.vy),self.w,self.h):
                self.y += sign(self.vy)
            
        if self.y==oy:
            self.gnd=True
        else:
            self.gnd=False
            
        self.updatecamera()
        
        # items
        
        global score
        
        if level.tile_at(self.x+self.w//2,self.y+self.h//2)==5: #emeralds
            level.set_tile(self.x+self.w//2,self.y+self.h//2,0xd)
            self.emeralds+=1
            score += 200
            g_sound.play_sfx(sfx.emerald, len(sfx.emerald), True)
            
        if level.tile_at(self.x+self.w//2,self.y+self.h//2)==8: #big fuel
            level.set_tile(self.x+self.w//2,self.y+self.h//2,0)
            self.fuel+=200
            if self.fuel > 200: self.fuel=200
            score += 200
            g_sound.play_sfx(sfx.fuel, len(sfx.fuel), True)
            
        if level.tile_at(self.x+self.w//2,self.y+self.h//2)==4: #coin
            level.set_tile(self.x+self.w//2,self.y+self.h//2,0)
            score += 200
            g_sound.play_sfx(sfx.fuel, len(sfx.fuel), True)
            
        #check win condition
        
        if level.tile_at(self.x,self.y+self.h//2)==12 and level.tile_at(self.x+self.w,self.y+self.h//2)==12: #door
            if self.emeralds==level.emeralds:
                g_sound.play_sfx(sfx.door, len(sfx.door), True)
                level.next()
                self.vx=0
                self.vy=0
                self.dir=1
                self.climb=False
                self.walk=False
                self.jp=0
                self.fuel=0
                self.f=0
                self.emeralds=0
                return
        
        # spikes collision
        if level.tile_at(self.x,self.y)==0:
            if level.collisionAtPosition(0xb, self.x,self.y, self.w, self.h-3 ): #ground spikes
                self.lives -= 1
                self.dead = True
                self.f=0
                g_sound.play_sfx(sfx.dead, len(sfx.dead), True)
        if level.tile_at(self.x,self.y)==0xb:
            if level.collisionAtPosition(0xb, self.x+5,self.y, self.w, self.h ): #ground spikes
                self.lives -= 1
                self.dead = True
                self.f=0
                g_sound.play_sfx(sfx.dead, len(sfx.dead), True)
                
        #enemies
        if self.enemiesCollision():
            self.lives -= 1
            self.dead = True
            self.f=0
            g_sound.play_sfx(sfx.dead, len(sfx.dead), True)

    def draw(self):
        if self.dead:
            screen.blit(player_death[self.f], self.x-camerax, self.y-cameray)

            return
            
        if self.climb:
            screen.blit(sprites.player8_climb, self.x-camerax, self.y-cameray)
            return
        if self.walk and frame%3==1:
            self.f+=1
            if self.f>2: self.f=0
            
        if not self.gnd:
            self.f=2
        
        if self.dir > 0:
            screen.blit(player_right[self.f], self.x-camerax, self.y-cameray)
            if self.jp > 0:
                screen.blit(flame[frame%3], self.x-camerax-1, self.y-cameray+6)
        else:
            screen.blit(player_left[self.f], self.x-camerax, self.y-cameray)
            if self.jp > 0:
                screen.blit(flame[frame%3], self.x-camerax+5, self.y-cameray+6)
            
        

# Player object
bots=[]        
balls=[]
springs=[]
missiles=[]
spikes=[]
p1 = Player(0,0)

level=Level()

intro=True
gameover=False
t_intro=50
outro=False
t_gameover=100
help=False
win=False

def print_border(txt,x,y,cf,cb):
    
    for i in range(-1,2):
        for j in range(-1,2):
           umachine.draw_text(x+i,y+j,txt,cb) 
           
    umachine.draw_text(x,y,txt,cf) 
    
def print_shadow(txt,x,y,cf,cb):
    
    umachine.draw_text(x,y+1,txt,cb) 
    umachine.draw_text(x,y,txt,cf) 


def reset():
    global p1
    global level
    global frame
    global score
    
    frame=0
    score=0
    
    p1 = Player(0,0)
    level=Level()


def draw_help(page):
    
    r=upg.Rect(0,0,scrwidth,scrheight+8)
    screen.fill(10,r)

    if page ==1:
        screen.blit(titlescreen.logo, 20, 2)
        print_shadow("Welcome to jetpack",2,20,3,8)
        print_shadow("you are a daring adventurer in search of precious gems. with your trusty jetpack\nyour quest is to take all the\ngems witout getting killed. collect treasure along the\nway to earn extra lives.\nfind fuel to make your\nsearch easier.",0,20+7,1,8)
    if page ==2:
        screen.blit(sprites.player8_3, 5, 5)
        screen.blit(sprites.player8_3l, 97, 5)
        print_border("Jetpack Model L1069-E",15,6,5,8)
        print_shadow("Your jetpack is a valuable\ntool in your quest for gems,\nfuel must be found before\nthe jet turbines will\nfunction",0,25,1,8)
    if page==3:
        print_shadow("Five different types of\nenemies will try to put an\nend to your quest",2,2,3,8)
        for i in range(5):
            r=upg.Rect(2,21+i*12,10,10)
            screen.fill(8,r)
            
        screen.blit(sprites.bot8_1, 3, 23)
        print_shadow("TRACKBOT",15,24,1,8)
        screen.blit(sprites.sball8, 3, 32+2)
        print_shadow("STEEL BALL",15,34+2,1,8)
        screen.blit(sprites.spring8_1, 3, 46)
        print_shadow("SPRING",15,48,1,8)
        screen.blit(sprites.missile8_Up, 3+1, 58)
        print_shadow("MISSILE",15,60,1,8)
        screen.blit(sprites.spikes8_1, 3+2, 72)
        print_shadow("SPIKES",15,72,1,8)
        
    if page==5:
        screen.blit(titlescreen.logo, 16, 2)
        umachine.draw_text(92,15,version,9)
        print_shadow("This game made by\n@bl_ackrain for the Pokitto\npython competition using the\nonline python editor",2,22,1,8)
        print_shadow("pyinsky.herokuapp.com",2,48,4,8)
        print_shadow("Thanks to @fmanga, @Hanski\nand @jonne for the fantastic Editor.",2,57,1,8)
        
def intro_update():
    global t_intro
    global outro
    global intro
    
    global help
    global help_page
    
    if t_intro > 0:
        t_intro-=1
    else:
        if help and (btns[4] or btns[5]):
            help_page += 1
            if help_page > 3:
                help=False
                t_intro=10
                return
            t_intro=30
            return
            
        if btns[4]:
            outro=True
            t_intro=80
        if btns[5]:
            help=True
            help_page=1
            t_intro=30
        if btns[6]:
            help=True
            help_page=5
            t_intro=30
            
        if outro and t_intro ==0:
            intro=False
            outro=False
            t_intro=50
            

def intro_draw():
    global t_intro
    global t_outro
    
    global help
    global help_page
    
    if help:
        draw_help(help_page)
        return
    
    c=[4,7,0xf,0xc]
    
    if t_intro <= 0:
        if frame%16 > 2:
            print_shadow("Press (A) to Start",22,45,1,11)
        print_shadow("(C):Credits",2,70,1,8)
        print_shadow("(B):Help",75,70,1,8)
        print_border("by @bl_ackrain 2019",3,80,1,11)
        umachine.draw_text(92,80,version,9)

    if outro:
        r=upg.Rect(30-((80-t_intro)//2),25+rnd(1),scrwidth-30+((80-t_intro)//2),3+rnd(2))
        screen.fill(c[rnd(2)],r)
            
        screen.blit(titlescreen.logo, 20-((80-t_intro)//2), 20+rnd(1))
    else:
        r=upg.Rect(30+(t_intro//3),25+rnd(1),scrwidth-30-(t_intro//3),3+rnd(2))
        screen.fill(c[rnd(2)],r)
            
        screen.blit(titlescreen.logo, 20+(t_intro//3), 20+rnd(1))
            
    
def gameover_update():
    global t_gameover
    global gameover
    global intro
    global t_intro
    global win
    
    if t_gameover > 0:
        t_gameover-=1
    else:
        gameover=False
        win=False
        reset()
        intro=True
        
def gameover_draw():
    global win
    if win:
        print_border("CONGRATURATION!!!",10,30,1,0xb)
        print_border("YOU HAVE COMPLETED",10,40,1,0xb)
        print_border("A GREAT GAME.",10,50,1,0xb)
        print_border("NOW GO AND REST OUR HERO!",10,60,1,0xb)
        return
    else:
        print_border("Game Over",40,30,1,0xb)
        
def game_update():
    
    for bot in bots:
        bot.update()
    for ball in balls:
        ball.update()
    for spr in springs:
        spr.update()
        missiles
    for msl in missiles:
        msl.update()
    for spk in spikes:
        spk.update()
        
    if level.newlvl:
        p1.updatecamera()
        return
    p1.update()
        
        
def game_draw():
    
    level.draw()
    p1.draw()
    
    for bot in bots:
        bot.draw()
    for ball in balls:
        ball.draw()
    for spr in springs:
        spr.draw()
    for msl in missiles:
        msl.draw()
    for spk in spikes:
        spk.draw()
    
    r=upg.Rect(0,scrheight,scrwidth,8)
    screen.fill(11,r)
    umachine.draw_text(2,scrheight+1,"F:",1)
    r=upg.Rect(10-1,scrheight+1,20+2,5)
    screen.fill(8,r)
    r=upg.Rect(10,scrheight+2,p1.fuel//10,3)
    screen.fill(5,r)
    umachine.draw_text(37,scrheight+1,"Lives:"+str(p1.lives),1)
    umachine.draw_text(74,scrheight+1,"S:"+'{:07d}'.format(score),1)
    
    if level.newlvl:
        if level.t_new > 0:
            level.t_new -=1
            
            if level.t_new < 25:
                h=15
            else:
                h=(30-(level.t_new))*3
            
            r=upg.Rect(0,30,scrwidth,h)
            screen.fill(8,r)
            
            if h==15:
                umachine.draw_text(25,35,"Level : "+'{:02d}/{:02d}'.format(level.lvl_nmbr+1,len(levels)),1)
    
        else:
            level.newlvl=False

def init():
    intro=True
    

def update():
    poll_btns()
    
    if intro:
        intro_update()
        return
    if gameover:
        gameover_update()
        return
    game_update()
    
    
def draw():
    if intro:
        intro_draw()
        return
    if gameover:
        gameover_draw()
        return
    
    game_draw()
    


init()

while True:
    frame +=1
    update()
    draw()
    upg.display.flip()
