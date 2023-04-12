"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

Author: Kevin Márquez
marquezberriosk@gmail.com

Author: Lewis Ochoa
lewis8a@gmail.com

This file contains the class BeginGameState.
"""
from typing import Dict, Any

import pygame

from gale.state_machine import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Player import Player
from src.Camera import Camera
from src.GameLevel import GameLevel

class BeginGameState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.score = enter_params.get("score", 0)
        self.transition_alpha = 255
        self.display_text = True
        self.circle = max(settings.VIRTUAL_HEIGHT, settings.VIRTUAL_WIDTH) * 1.25

        # A surface that supports alpha for the screen
        self.screen_alpha_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), pygame.SRCALPHA
        )
        
        self.camera = enter_params.get(
            "camera", Camera(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        self.game_level = enter_params.get("game_level")
        if self.game_level is None:
            self.game_level = GameLevel(self.level, self.camera)

        self.tilemap = self.game_level.tilemap
        if self.level == 1:
            self.player = Player(0, settings.VIRTUAL_HEIGHT - 66, self.game_level)
        elif self.level == 2:
            self.player = Player(16 * 2, 16 * 5, self.game_level)
        elif self.level == 3:
            self.player = Player(16 * 2, 16 * 5, self.game_level)

        def arrive_after():
            # Then, animate the text going disapear
            self.display_text = False
            Timer.tween(
               1,
               [(self, {"transition_alpha": 0})],
               # We are ready to play
               on_finish=lambda: self.state_machine.change(
                   "play",
                   level=self.level,
                   player=self.player,
                   game_level=self.game_level,
                   camera=self.camera
               ),
            )

        #Fade out
        Timer.after(
                1,
                arrive_after
            )

    def render(self, surface: pygame.Surface) -> None:
        world_surface = pygame.Surface((self.tilemap.width, self.tilemap.height))
        self.game_level.render(world_surface)
        self.player.render(world_surface)
        surface.blit(world_surface, (-self.camera.x, -self.camera.y))

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {30}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        pygame.draw.circle(
            self.screen_alpha_surface,
            (0, 0, 0, self.transition_alpha),
            (0,0),
            self.circle,
        )

        if self.display_text:
            render_text(
                self.screen_alpha_surface,
                f"Level {self.level}",
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH / 2 - 50,
                settings.VIRTUAL_HEIGHT/ 2 - 10,
                (255, 255, 255),
                shadowed=True,
            )

        surface.blit(self.screen_alpha_surface, (0, 0))