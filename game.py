"""
2D Local Fighting Game (Pygame)

Run:
  - Install pygame: pip install pygame
  - python 2D_fighting_game_pygame.py

Description:
  - Local 2-player fighting game (keyboard vs keyboard)
  - Simple state machine: idle, walk, jump, attack, hurt, knockdown
  - Hitbox/hurtbox collision for attacks
  - Health bars, round system, simple win/lose
  - Placeholder rectangle art; easily replaced with sprites

Controls:
  Player 1 (Left):
    A / D: move left/right
    W: jump
    S: crouch
    F: light attack
    G: heavy attack

  Player 2 (Right):
    LEFT / RIGHT: move
    UP: jump
    DOWN: crouch
    K: light attack
    L: heavy attack

  Misc:
    R: restart round
    ESC: quit

This is an educational example, not a production engine.
"""

import pygame
import sys
import math
from enum import Enum

# ----- CONFIG -----
SCREEN_W = 1000
SCREEN_H = 600
FPS = 60
TILE = 32
GRAVITY = 0.8
GROUND_Y = SCREEN_H - 120

PLAYER_WIDTH = 48
PLAYER_HEIGHT = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (30, 30, 40)
P1_COLOR = (200, 80, 80)
P2_COLOR = (80, 120, 200)
HEALTH_BG = (60, 60, 60)

# Gameplay
WALK_SPEED = 3.5
JUMP_SPEED = -14
ATTACK_DURATION = 18  # frames
HURT_DURATION = 20
INVULN_DURATION = 30
BLOCK_STUN = 10

MAX_HEALTH = 100

# ----- ENUMS -----


class State(Enum):
    IDLE = 0
    WALK = 1
    JUMP = 2
    FALL = 3
    CROUCH = 4
    ATTACK = 5
    HURT = 6
    DOWN = 7


class Facing(Enum):
    LEFT = -1
    RIGHT = 1

# ----- PLAYER CLASS -----


class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.controls = controls
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.state = State.IDLE
        self.facing = Facing.RIGHT
        self.health = MAX_HEALTH
        self.attack_timer = 0
        self.hurt_timer = 0
        self.invuln_timer = 0
        self.blocking = False
        self.combo = 0
        self.rounds = 0

    def center(self):
        return self.rect.centerx, self.rect.centery

    def update(self, keys, opponent):
        # timers
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            if self.hurt_timer == 0:
                if self.health <= 0:
                    self.state = State.DOWN
                else:
                    self.state = State.IDLE
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0 and self.state == State.ATTACK:
                self.state = State.IDLE
        # movement disabled while hurt or down
        if self.state == State.HURT or self.state == State.DOWN:
            self.apply_gravity()
            self.rect.x += int(self.vx)
            self.rect.y += int(self.vy)
            self.collide_ground()
            return

        # input
        move = 0
        if keys[self.controls['left']]:
            move -= 1
        if keys[self.controls['right']]:
            move += 1
        if move != 0:
            self.vx = move * WALK_SPEED
            self.state = State.WALK
            self.facing = Facing.RIGHT if move > 0 else Facing.LEFT
        else:
            self.vx = 0
            if self.on_ground and self.state != State.ATTACK:
                self.state = State.IDLE

        if keys[self.controls['jump']] and self.on_ground:
            self.vy = JUMP_SPEED
            self.on_ground = False
            self.state = State.JUMP

        # crouch (simple)
        if keys[self.controls['crouch']] and self.on_ground:
            self.state = State.CROUCH
            self.vx = 0

        # attacks
        if keys[self.controls['light']] and self.attack_timer == 0:
            self.start_attack('light')
        if keys[self.controls['heavy']] and self.attack_timer == 0:
            self.start_attack('heavy')

        # apply movement
        self.rect.x += int(self.vx)
        self.apply_gravity()
        self.rect.y += int(self.vy)
        self.collide_ground()

        # collisions with opponent's hurtboxes
        if self.state == State.ATTACK and self.attack_timer > 0:
            hb = self.get_hitbox()
            if hb.colliderect(opponent.get_hurtbox()):
                # hit!
                if opponent.invuln_timer == 0 and opponent.state != State.DOWN:
                    damage = 6 if self.attack_type == 'light' else 12
                    # simple block check: if opponent is crouching and facing away from attack, reduce
                    blocked = False
                    if opponent.state == State.CROUCH:
                        blocked = True
                    if blocked:
                        opponent.hurt_timer = BLOCK_STUN
                        opponent.vx = 0
                        opponent.vy = 0
                        opponent.invuln_timer = INVULN_DURATION
                    else:
                        opponent.health -= damage
                        opponent.hurt_timer = HURT_DURATION
                        # knockback
                        kb = 6 if self.attack_type == 'light' else 12
                        dir = 1 if self.facing == Facing.RIGHT else -1
                        opponent.vx = kb * dir
                        opponent.vy = -6
                        opponent.invuln_timer = INVULN_DURATION
                    # prevent repeated hits in same attack window
                    self.attack_timer = min(self.attack_timer, 4)

    def start_attack(self, typ):
        self.state = State.ATTACK
        self.attack_timer = ATTACK_DURATION
        self.attack_type = typ

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > 20:
            self.vy = 20

    def collide_ground(self):
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def get_hurtbox(self):
        # slightly smaller than rect
        hb = self.rect.inflate(-8, -12)
        return hb

    def get_hitbox(self):
        # create a hitbox in front of player depending on attack type
        reach = 40 if self.attack_type == 'light' else 60
        w = reach
        h = 30
        if self.facing == Facing.RIGHT:
            x = self.rect.right
        else:
            x = self.rect.left - w
        y = self.rect.centery - h//2
        return pygame.Rect(x, y, w, h)

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.state = State.IDLE
        self.health = MAX_HEALTH
        self.attack_timer = 0
        self.hurt_timer = 0
        self.invuln_timer = 0

# ----- GAME LOOP -----


def draw_health_bar(surf, x, y, w, h, pct, name, color):
    pygame.draw.rect(surf, HEALTH_BG, (x, y, w, h))
    inner_w = max(0, int(w * (pct/100.0)))
    pygame.draw.rect(surf, color, (x, y, inner_w, h))
    # border
    pygame.draw.rect(surf, WHITE, (x, y, w, h), 2)
    # name
    font = pygame.font.SysFont('consolas', 18)
    txt = font.render(name, True, WHITE)
    surf.blit(txt, (x+4, y-22))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('2D Fighting Game - Pygame')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('consolas', 24)

    # controls mapping
    p1_controls = {
        'left': pygame.K_a,
        'right': pygame.K_d,
        'jump': pygame.K_w,
        'crouch': pygame.K_s,
        'light': pygame.K_f,
        'heavy': pygame.K_g
    }
    p2_controls = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'jump': pygame.K_UP,
        'crouch': pygame.K_DOWN,
        'light': pygame.K_k,
        'heavy': pygame.K_l
    }

    p1 = Player(200, GROUND_Y-PLAYER_HEIGHT, P1_COLOR, p1_controls)
    p2 = Player(700, GROUND_Y-PLAYER_HEIGHT, P2_COLOR, p2_controls)

    round_active = True
    winner = None
    round_timer = 0

    while True:
        dt = clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    p1.reset(200, GROUND_Y-PLAYER_HEIGHT)
                    p2.reset(700, GROUND_Y-PLAYER_HEIGHT)
                    round_active = True
                    winner = None

        if round_active:
            p1.update(keys, p2)
            p2.update(keys, p1)

            # basic clamp to stage
            p1.rect.left = max(20, min(p1.rect.left, SCREEN_W-20-PLAYER_WIDTH))
            p2.rect.left = max(20, min(p2.rect.left, SCREEN_W-20-PLAYER_WIDTH))

            # check deaths
            if p1.health <= 0 or p2.health <= 0:
                round_active = False
                winner = 'Player 1' if p2.health <= 0 else 'Player 2'
                round_timer = pygame.time.get_ticks()

        # draw
        screen.fill(BG_COLOR)
        # ground
        pygame.draw.rect(screen, (50, 50, 60),
                         (0, GROUND_Y, SCREEN_W, SCREEN_H-GROUND_Y))

        # players (with simple flash if invuln)
        def draw_player(pl):
            alpha = 255
            if pl.invuln_timer > 0 and (pl.invuln_timer//3) % 2 == 0:
                # flash
                s = pygame.Surface(
                    (pl.rect.width, pl.rect.height), pygame.SRCALPHA)
                s.fill((255, 255, 255, 100))
                screen.blit(s, (pl.rect.x, pl.rect.y))
            pygame.draw.rect(screen, pl.color, pl.rect)
            # draw hurtbox
            hb = pl.get_hurtbox()
            pygame.draw.rect(screen, (0, 0, 0), hb, 1)
            # draw hitbox for active attacks
            if pl.state == State.ATTACK and pl.attack_timer > 0:
                hb2 = pl.get_hitbox()
                pygame.draw.rect(screen, (255, 255, 0), hb2, 2)

        draw_player(p1)
        draw_player(p2)

        # HUD
        draw_health_bar(screen, 40, 30, 380, 24, p1.health, 'P1', P1_COLOR)
        draw_health_bar(screen, SCREEN_W-420, 30, 380,
                        24, p2.health, 'P2', P2_COLOR)

        if not round_active:
            info = font.render(
                f'{winner} wins! Press R to restart.', True, WHITE)
            screen.blit(
                info, (SCREEN_W//2 - info.get_width()//2, SCREEN_H//2 - 20))

        # Controls hint
        hint = font.render(
            'P1: A/D W S  F/G  |  P2: ←/→ ↑ ↓  K/L  |  R restart', True, WHITE)
        screen.blit(hint, (SCREEN_W//2 - hint.get_width()//2, SCREEN_H - 40))

        pygame.display.flip()


if __name__ == '__main__':
    main()
