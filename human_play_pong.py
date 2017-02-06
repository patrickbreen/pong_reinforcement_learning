import sys
import shutil
import os

import pygame
import numpy as np

# parameters
size = width, height = (280, 200)
wait = 10
black = (0, 0, 0)
velocity = [1, 1]
goals_scored = 0
frame_capture = 10

# set up objects
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.jpeg")
ball = pygame.transform.scale(ball, (20, 20))
ballrect = ball.get_rect()
ballrect = ballrect.move([20, 20])

pad1 = pygame.image.load("paddle.jpeg")
pad1 = pygame.transform.scale(pad1, (15, 40))
padrect1 = pad1.get_rect()
padrect1 = padrect1.move([0, 70])

pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 16)

# clear saved gameplay
shutil.rmtree("saved_gameplay/actions", ignore_errors=True)
os.mkdir("saved_gameplay/actions") 
shutil.rmtree("saved_gameplay/screens", ignore_errors=True)
os.mkdir("saved_gameplay/screens") 

# convert hex string representation of screen to numpy array
def get_img_mat_from_hex(screen):
  screen = screen.strip()

  red_ar = np.empty((width,height), dtype=np.float16)
  green_ar = np.empty((width,height), dtype=np.float16)
  blue_ar = np.empty((width,height), dtype=np.float16)

  row = 0
  col = 0

  for start in range(0, len(screen), 8):
    red_ar[row, col] = int(screen[start:start+2], 16)
    green_ar[row, col] = int(screen[start+2:start+4], 16)
    blue_ar[row, col] = int(screen[start+4:start+6], 16)

    if row < width-1:
      row += 1
    else:
      col += 1
      row = 0
      
  red_ar = red_ar.T
  green_ar = green_ar.T
  blue_ar = blue_ar.T

  return np.concatenate((red_ar[...,np.newaxis],green_ar[...,np.newaxis], blue_ar[...,np.newaxis]),axis=2)

# game loop
frame = 0

# action holds the player action
# 0 is no action, 1 is up, -1 is down
action = 0

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  # update ball
  ballrect = ballrect.move(velocity)
  pygame.time.wait(wait)

  # case where player deflects the ball
  if ballrect.left < padrect1.right and \
    (
        (padrect1.bottom > ballrect.bottom and ballrect.bottom > padrect1.top)
        or
        (padrect1.bottom < ballrect.top and ballrect.top < padrect1.top)
    ):
    velocity[0] = -velocity[0]
    velocity[1] = -velocity[1]


  # case where ball scores
  if ballrect.left < 0:
    goals_scored += 1
    velocity[0] = -velocity[0]

  # cases where ball hits walls
  if ballrect.right > width:
    velocity[0] = -velocity[0]

  if ballrect.top < 0 or ballrect.bottom > height:
    velocity[1] = -velocity[1]

  # update player 1
  keys = pygame.key.get_pressed()
  if keys[pygame.K_UP] and padrect1.top > 0:
    padrect1 = padrect1.move([0, -1])
    action = [1, 0, 0]
  elif keys[pygame.K_DOWN] and padrect1.bottom < height:
    padrect1 = padrect1.move([0, 1])
    action = [0, 1, 0]
  else:
    action = [0, 0, 1]

  # update score
  score_surface = myfont.render("goals scored = " + str(goals_scored), False, (255, 255, 255))

  # draw things to screen
  screen.fill(black)
  screen.blit(ball, ballrect)
  screen.blit(pad1, padrect1)
  screen.blit(score_surface, (70, 50))
  pygame.display.flip()

  # capture screen, action and score every "frame_capture" frames
  if frame % frame_capture == 0:
    screen_str = pygame.image.tostring(screen, "RGBX").hex()
    np_array_action = np.array(action)
    np.save("saved_gameplay/actions/" + str(frame), np_array_action)
    with open("saved_gameplay/scores.txt", "w") as f:
      f.write(str(goals_scored) + "\n")
    np_array_screen = get_img_mat_from_hex(screen_str)
    np.save("saved_gameplay/screens/" + str(frame), np_array_screen)

  frame += 1

