import pygame

class Paddles:
    def __init__(self,game):
        self.leftpv=0
        self.rightpv=0
        self.pheight=60
        self.pwidth=10
        self.leftpp=game.height/2
        self.rightpp=game.height/2
        self.game=game
    def reset(self):
        self.leftpp=game.height/2
        self.rightpp=game.height/2
    def setleftpv(self,v):
        self.leftpv=v
    def setrightpv(self,v):
        self.rightpv=v
    def move(self):
        newleftp=self.leftpp+self.leftpv
        newrightp=self.rightpp+self.rightpv
        if newleftp>self.pheight/2 and newleftp<self.game.height-self.pheight/2:
            self.leftpp=newleftp
        if newrightp>self.pheight/2 and newrightp<self.game.height-self.pheight/2:
            self.rightpp=newrightp
        pygame.draw.line(game.screen,game.BLACK,(self.pwidth,0),(self.pwidth,self.game.height),2)
        pygame.draw.line(game.screen,game.BLACK,(self.game.width-self.pwidth,0),(self.game.width-self.pwidth,self.game.height),2)
        pygame.draw.line(game.screen,game.WHITE,(self.game.width/2,0),(self.game.width/2,self.game.height),2)
        pygame.draw.rect(game.screen,game.BLUE,(self.game.width-self.pwidth,self.rightpp-self.pheight/2,self.game.width,self.pheight))
        pygame.draw.rect(game.screen,game.BLUE,(0,self.leftpp-self.pheight/2,self.pwidth,self.pheight))
                                                                                                                                   

class Ball:
    def __init__(self,game):
        self.game=game
        self.ballradius=10
        self.ballx=self.game.width/2
        self.bally=self.game.height/2
        self.ballxv=0
        self.ballyv=0
    def restart(self):
        self.ballxv=0
        self.ballyv=0
    def velocity(self,x,y):
        self.ballxv=x
        self.ballyv=y
    def move(self):
        newx=self.ballx+self.ballxv
        newy=self.bally+self.ballyv
        #if newx-self.ballradius<0 or newx+self.ballradius>self.game.width:
            #self.ballxv*=-1
            #newx=newx-(newx-self.ballx)+self.ballxv
        if newx-self.ballradius<game.paddles.pwidth or newx+self.ballradius>self.game.width-self.game.paddles.pwidth:
            self.ballxv*=-1
            newx=newx-(newx-self.ballx)+self.ballxv
            if newx<self.game.width/2:
                if self.bally<self.game.paddles.leftpp-self.game.paddles.pheight/2 or self.bally>self.game.paddles.leftpp+self.game.paddles.pheight/2:
                    self.game.rightscore+=1
                    newx=game.width/2
                else:
                    self.ballyv+=self.game.paddles.leftpv
            else:
                if self.bally<self.game.paddles.rightpp-self.game.paddles.pheight/2 or self.bally>self.game.paddles.rightpp+self.game.paddles.pheight/2:
                    self.game.leftscore+=1
                    newx=game.width/2
                else:
                    self.ballyv+=self.game.paddles.rightpv
        if newy-self.ballradius<0 or newy+self.ballradius>self.game.height:
            self.ballyv*=-1
            newy=newy-(newy-self.bally)+self.ballyv
        self.ballx=newx
        self.bally=newy
        pygame.draw.circle(game.screen,game.YELLOW,[int(self.ballx),int(self.bally)],self.ballradius)

class Pong:
    def __init__(self):
        self.YELLOW=(255,255,0)
        self.BLUEGRAY=(170,170,175)
        self.BLACK=(0,0,0)
        self.WHITE=(255,255,255)
        self.BLUE=(0,0,255)
        self.RED=(255,0,0)
        self.width=800
        self.height=400
        self.screen=pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Pong")
        self.playing=False
        self.paddles=Paddles(self)
        self.ball=Ball(self)
        self.ball.velocity(3,-1)
        self.leftscore=0
        self.rightscore=0
        self.scorewidth=10
        self.scoreheight=30
    def go(self):
        pygame.init()
        self.playing=True
        clock=pygame.time.Clock()
        while self.playing:
            #self.restart()
            while True:
                for event in pygame.event.get():
                    self.playing=True
                    if event.type==pygame.QUIT:
                        self.playing=False
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_ESCAPE:
                            self.playing=False
                        elif event.key==pygame.K_UP:
                            self.paddles.setrightpv(-4)
                        elif event.key==pygame.K_DOWN:
                            self.paddles.setrightpv(4)
                        elif event.key==pygame.K_w:
                            self.paddles.setleftpv(-4)
                        elif event.key==pygame.K_s:
                            self.paddles.setleftpv(4)
                    if event.type==pygame.KEYUP:
                        if event.key in (pygame.K_UP,pygame.K_DOWN):
                            self.paddles.setrightpv(0)
                        elif event.key in (pygame.K_w,pygame.K_s):
                            self.paddles.setleftpv(0)
                if not self.playing:
                    break
                self.screen.fill(self.BLUEGRAY)
                self.paddles.move()
                self.ball.move()
                font=pygame.font.SysFont("Courier", 25, True, False)
                sl=font.render(str(self.leftscore),True, self.WHITE)
                sr=font.render(str(self.rightscore),True, self.WHITE)
                self.screen.blit(sl,(self.width/2-self.scorewidth*3,self.scoreheight))
                self.screen.blit(sr,(self.width/2+self.scorewidth*2,self.scoreheight))
                pygame.display.flip()
                clock.tick(45)
                if max(self.rightscore,self.leftscore)>10:
                    font=pygame.font.SysFont("Calibri",50,True,False)
                    winner=font.render("winner",True,self.RED)
                    self.screen.blit(winner,(self.width/2-8*20,self.height/2))
                    self.playing=False
                    break
            font=pygame.font.SysFont("Calibri",50,True,False)
            again=font.render("do you want to play again?",True,self.WHITE)
            self.screen.blit(again,(self.width/2-12*20,self.height-3*24))
            pygame.display.flip()
            self.playing=None
            while self.playing is None:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        self.playing=False
                        break
                    if event.type==pygame.KEYDOWN:
                        if event.key in (pygame.K_n,pygame.K_ESCAPE):
                            self.playing=False
                        elif event.key in (pygame.K_y,pygame.K_RETURN):
                            self.playing=False
                    if event.type==pygame.KEYUP:
                        if event.key in (pygame.K_n,pygame.K_ESCAPE,pygame.K_y,pygame.K_RETURN):
                            break
                        else:
                            self.playing=None
        pygame.quit()

game=Pong()
game.go()

#.wav file ball sound effect
# mp3 background music
