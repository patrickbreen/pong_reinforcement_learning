import sys

import pygame

# params
size = width, height = (700, 500)
wait = 1
black = (0, 0, 0)

# set up objects
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.jpeg")
ball = pygame.transform.scale(ball, (25, 25))
ballrect = ball.get_rect()
ballrect = ballrect.move([100, 100])

paddle1 = pygame.image.load("paddle.jpeg")
paddle1 = pygame.transform.scale(paddle1, (30, 100))
paddlerect1 = paddle1.get_rect()
paddlerect1 = paddlerect1.move([0, 100])

velocity = [1, 1]

goals_scored = 0

pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 30)

# game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  # update ball
  ballrect = ballrect.move(velocity)
  pygame.time.wait(wait)

  # case where player deflects
  if ballrect.left < paddlerect1.right and \
    (
        (paddlerect1.bottom > ballrect.bottom and ballrect.bottom > paddlerect1.top)
        or
        (paddlerect1.bottom < ballrect.top and ballrect.top < paddlerect1.top)
    ):
    velocity[0] = -velocity[0]
    velocity[1] = -velocity[1]


  # case where ball scores
  if ballrect.left < 0:
    goals_scored += 1
    velocity[0] = -velocity[0]

  if ballrect.right > width:
    velocity[0] = -velocity[0]

  if ballrect.top < 0 or ballrect.bottom > height:
    velocity[1] = -velocity[1]

  # update player 1
  keys = pygame.key.get_pressed()
  if keys[pygame.K_UP] and paddlerect1.top > 0:
    paddlerect1 = paddlerect1.move([0, -1])
  if keys[pygame.K_DOWN] and paddlerect1.bottom < height:
    paddlerect1 = paddlerect1.move([0, 1])

  # update score
  score_surface = myfont.render("goals scored = " + str(goals_scored), False, (255, 255, 255))

  # draw things to screen
  screen.fill(black)
  screen.blit(ball, ballrect)
  screen.blit(paddle1, paddlerect1)
  screen.blit(score_surface, (350, 250))
  pygame.display.flip()

