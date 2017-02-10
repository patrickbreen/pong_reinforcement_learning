import sys
import shutil
import os
import random

import pygame
import numpy as np

class MyPongEnv:
    def __init__(self):
        # parameters
        self.size = self.width, self.height = (280, 200)
        self.wait = 10
        self.black = (0, 0, 0)
        self.velocity = [1, 1]
        self.goals_scored = 0
        self.frame_capture = 10
        self.frame = 0
        self.STATE_SIZE = 3

        # set up objects
        self.screen = pygame.display.set_mode(self.size)

        self.ball = pygame.image.load("ball.jpeg")
        self.ball = pygame.transform.scale(self.ball, (20, 20))
        self.ballrect = self.ball.get_rect()
        self.ballrect = self.ballrect.move([20, 20])

        self.pad1 = pygame.image.load("paddle.jpeg")
        self.pad1 = pygame.transform.scale(self.pad1, (15, 40))
        self.padrect1 = self.pad1.get_rect()
        self.padrect1 = self.padrect1.move([0, 70])

        pygame.font.init()
        self.myfont = pygame.font.SysFont("Comic Sans MS", 16)

        # clear saved gameplay
        shutil.rmtree("saved_gameplay/actions", ignore_errors=True)
        os.mkdir("saved_gameplay/actions")
        shutil.rmtree("saved_gameplay/screens", ignore_errors=True)
        os.mkdir("saved_gameplay/screens")

        self.score_surface = self.myfont.render(
            "goals scored = " + str(self.goals_scored), False, (255, 255, 255))


    def step(self, action):

        # convert hex string representation of screen to numpy array
        def get_img_mat_from_hex(screen, width, height):
            screen = screen.strip()

            red_ar = np.empty((width, height), dtype=np.float16)
            green_ar = np.empty((width, height), dtype=np.float16)
            blue_ar = np.empty((width, height), dtype=np.float16)

            row = 0
            col = 0

            for start in range(0, len(screen), 8):
                red_ar[row, col] = int(screen[start:start + 2], 16)
                green_ar[row, col] = int(screen[start + 2:start + 4], 16)
                blue_ar[row, col] = int(screen[start + 4:start + 6], 16)

                if row < width - 1:
                    row += 1
                else:
                    col += 1
                    row = 0

            red_ar = red_ar.T
            green_ar = green_ar.T
            blue_ar = blue_ar.T

            return np.concatenate((red_ar[..., np.newaxis], green_ar[..., np.newaxis], blue_ar[..., np.newaxis]), axis=2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # update ball
        self.ballrect = self.ballrect.move(self.velocity)
        pygame.time.wait(self.wait)

        # case where player deflects the ball
        if self.ballrect.left < self.padrect1.right and \
                (
                    (self.padrect1.bottom > self.ballrect.bottom and self.ballrect.bottom > self.padrect1.top)
                    or
                    (self.padrect1.bottom < self.ballrect.top and self.ballrect.top < self.padrect1.top)
                ):
            self.velocity[0] = -self.velocity[0]
            self.velocity[1] = -self.velocity[1]

        # case where ball scores
        if self.ballrect.left < 0:
            reward = -100
            self.goals_scored += 1
            self.velocity[0] = -self.velocity[0]
        else:
            reward = 0

        # cases where ball hits walls
        if self.ballrect.right > self.width:
            self.velocity[0] = -self.velocity[0]

        if self.ballrect.top < 0 or self.ballrect.bottom > self.height:
            self.velocity[1] = -self.velocity[1]

        # update paddle based on "action"
        if action[0] == 1:
            self.padrect1 = self.padrect1.move([0, -1])
        elif action[1] == 1:
            self.padrect1 = self.padrect1.move([0, 1])

        # update score
        self.score_surface = self.myfont.render(
            "goals scored = " + str(self.goals_scored), False, (255, 255, 255))

        # np.save("saved_gameplay/screens/" + str(frame), np_array_screen)
        # np_array_action = np.array(action)
        # np.save("saved_gameplay/actions/" + str(frame), np_array_action)
        # with open("saved_gameplay/scores.txt", "w") as f:
        #     f.write(str(goals_scored) + "\n")

        # if state is screen
        # screen_str = pygame.image.tostring(self.screen, "RGBX").hex()
        # new_state = get_img_mat_from_hex(screen_str, self.width, self.height)

        # if state is ball position and paddle position
        new_state = np.array([self.ballrect.right, self.ballrect.top, self.padrect1.top])

        done = False

        if self.goals_scored == 4:
            done = True

        return new_state, reward, done

    def sample_action_space(self):
        possible_actions = [
            np.array([1,0,0]),
            np.array([0,1,0]),
            np.array([0,0,1])
        ]
        return random.sample(possible_actions, 1)[0]

    def reset(self):
        self.__init__()
        return np.array([self.ballrect.right, self.ballrect.top, self.padrect1.top])

    def render(self):
        # draw things to screen
        self.screen.fill(self.black)
        self.screen.blit(self.ball, self.ballrect)
        self.screen.blit(self.pad1, self.padrect1)
        self.screen.blit(self.score_surface, (70, 50))
        pygame.display.flip()

    def human_player_input(self):
        # update player 1 (plug in a computer player here)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.padrect1.top > 0:
            action = np.array([1, 0, 0])
        elif keys[pygame.K_DOWN] and self.padrect1.bottom < self.height:
            action = np.array([0, 1, 0])
        else:
            action = np.array([0, 0, 1])
        return action


if __name__ == "__main__":
    # human player
    env = MyPongEnv()

    while True:
        action = env.human_player_input()
        new_state, reward, done = env.step(action)

        if env.frame % 20 == 0:
            env.render()