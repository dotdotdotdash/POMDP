# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
pygame.init()
import sys
from lib import *
import numpy as np

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Flight control')
screen.fill(0x222222)
   
# Initialise Dials.
horizon = Horizon(170,180)
turn = TurnCoord(20,180,150,150)
throttle = Generic(470,180,150,150)
#RXbattery = Battery(470,180,75,75)
#TXbattery = Battery(545,180,75,75)

max_velocity = 800
wing_area = 5825
max_altitude = 45100
act_dynamics = 0.1

#time parameters
resolution = 0.01
time = 0
sim_time = 40
iter = 0

#throttle position simulation
throttle_pos = []
i = 0
prev_throttle_pos = 0
prev_max_velocity = 0

#velocity calculation
#throttle_pos = get throttle position from keyboard or joystick

while i<=sim_time:
      if i > 0 and i <= 0.2*sim_time:
          throttle_pos.append(0.1)
      elif i > 0.2*sim_time and i <= 0.4*sim_time:
          throttle_pos.append(0.3)
      elif i > 0.4*sim_time and i <= 0.6*sim_time:
          throttle_pos.append(0.5)
      elif i > 0.6*sim_time and i <= 0.8*sim_time:
          throttle_pos.append(0.7)
      else:
          throttle_pos.append(1)
#      throttle_pos.append(0.3)
      i = i+resolution    

while 1:
   for event in pygame.event.get():
       if event.type == QUIT:
           pygame.quit()

   curPos = pygame.mouse.get_pos()
      
   if(curPos):
      horizon.update(screen, 127 - curPos[0]/2, 127 - curPos[1]/2 )
      turn.update(screen, (curPos[0]/2 - 127)/2, 127)
      if iter == len(throttle_pos):
          iter = 0
          
      if iter == 0:
            prev_throttle_pos = throttle_pos[iter]
            
      if prev_throttle_pos == throttle_pos[iter]:
            time = time + resolution
      else:
            time = 0
            prev_max_velocity = max_velocity*prev_throttle_pos
          
      sat_velocity = max_velocity*throttle_pos[iter]
      velocity_func = act_dynamics*time
      velocity = prev_max_velocity + sat_velocity*(velocity_func)**2
      if velocity >= sat_velocity:
           velocity = sat_velocity
      prev_throttle_pos = throttle_pos[iter]
      
      velocity = (velocity/max_velocity)*(290)
#      print velocity
      velocity = velocity + np.random.normal(0,0.1)
      throttle.update(screen, int(velocity-180))
      iter = iter + 1
#      RXbattery.update(screen, (data['RX_batt_volt'] - 115))
#      TXbattery.update(screen, 12.5*(data['TX_batt_volt'] - 105))
      pygame.display.update()
