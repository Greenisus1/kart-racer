#!/usr/bin/env python3
"""Original offline top-down kart-style time trial, no branded assets."""
import curses,math,random,time
from ui import put,run
class Racer:
 def __init__(self,seed=0):self.x=0.;self.progress=0.;self.speed=0.;self.health=5;self.score=0;self.rng=random.Random(seed);self.objects=[(i*40+30,self.rng.choice((-0.65,0,0.65)),self.rng.choice(('coin','rival','boost'))) for i in range(30)];self.passed=set()
 def step(self,dt,steer=0,gas=False,brake=False):
  dt=min(.1,max(0,dt));self.speed=max(0,min(38,self.speed+(16 if gas else -5)*dt-(28*dt if brake else 0)));self.x=max(-1.2,min(1.2,self.x+steer*1.5*dt));old=self.progress;self.progress+=self.speed*dt
  if abs(self.x)>1:self.speed*=.93
  for i,(distance,x,kind) in enumerate(self.objects):
   if i not in self.passed and old<=distance<=self.progress:
    self.passed.add(i)
    if abs(x-self.x)<.32:
     if kind=='coin':self.score+=1
     elif kind=='boost':self.speed=min(45,self.speed+12)
     else:self.health-=1;self.speed*=.45
  return self.progress>=1250 or self.health<=0

def loop(s):
 s.timeout(40);g=Racer();last=time.monotonic();paused=False;gas=False;done=False
 while True:
  h,w=s.getmaxyx();key=s.getch();now=time.monotonic();dt=now-last;last=now
  if key in (27,ord('q')):return
  if key==ord('r'):g=Racer();done=False;gas=False
  if key==ord(' '):paused=not paused
  if key in (ord('w'),curses.KEY_UP):gas=True
  if key in (ord('s'),curses.KEY_DOWN):gas=False
  if w>=40 and h>=18 and not paused and not done:done=g.step(dt,-1 if key in (ord('a'),curses.KEY_LEFT) else 1 if key in (ord('d'),curses.KEY_RIGHT) else 0,gas,key in (ord('s'),curses.KEY_DOWN))
  s.erase();put(s,0,1,'KART TIME TRIAL  distance '+str(int(g.progress))+'/1250  speed '+str(int(g.speed))+'  lives '+str(g.health)+' coins '+str(g.score),curses.A_BOLD)
  if w<40 or h<18:put(s,2,1,'Resize to40x18.')
  else:
   road=max(10,w//2);center=w//2
   for row in range(2,h-3):
    bend=int(math.sin((g.progress+(h-row)*8)/130)*(w//8));left=center-road//2+bend;right=left+road
    put(s,row,max(0,left),'│');put(s,row,min(w-2,right),'│')
    if int(g.progress/8+row)%3==0:put(s,row,center+bend,'┆')
   for i,(distance,x,kind) in enumerate(g.objects):
    ahead=distance-g.progress
    if i not in g.passed and 0<ahead<(h-7)*8:
     row=h-5-int(ahead/8);bend=int(math.sin((g.progress+(h-row)*8)/130)*(w//8));put(s,row,center+bend+int(x*road/2),{'coin':'◇','rival':'[R]','boost':'↑'}[kind])
   row=h-5;bend=int(math.sin((g.progress+(h-row)*8)/130)*(w//8));put(s,row,center+bend+int(g.x*road/2),'[P]',curses.A_REVERSE)
   if done:put(s,h//2,max(1,w//2-12),'FINISH! R restarts' if g.health>0 else 'CRASHED! R restarts',curses.A_REVERSE)
   elif paused:put(s,h//2,w//2,'PAUSED')
  put(s,h-1,1,'W/up throttle | A/D steer | S brake | Space pause | R restart | Esc/q exit');s.refresh()
if __name__=='__main__':
 import sys
 if '--version' in sys.argv:print('1.0.0')
 else:raise SystemExit(run(loop))
