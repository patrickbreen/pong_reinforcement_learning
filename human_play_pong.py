import sys

import pygame

# parameters
size = width, height = (140, 100)
wait = 10
black = (0, 0, 0)
velocity = [1, 1]
goals_scored = 0
frame_capture = 5

# set up objects
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.jpeg")
ball = pygame.transform.scale(ball, (5, 5))
ballrect = ball.get_rect()
ballrect = ballrect.move([10, 10])

pad1 = pygame.image.load("paddle.jpeg")
pad1 = pygame.transform.scale(pad1, (5, 14))
padrect1 = pad1.get_rect()
padrect1 = padrect1.move([0, 70])

pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 10)

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
    action = 1
  elif keys[pygame.K_DOWN] and padrect1.bottom < height:
    padrect1 = padrect1.move([0, 1])
    action = -1
  else:
    action = 0

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
    with open("saved_gameplay/actions.txt", "a") as f:
      f.write(str(action) + "\n")
    with open("saved_gameplay/scores.txt", "a") as f:
      f.write(str(goals_scored) + "\n")
    with open("saved_gameplay/screens.txt", "a") as f:
      f.write(screen_str + "\n")

  frame += 1

