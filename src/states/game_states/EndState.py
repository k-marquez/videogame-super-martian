"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

Author: Kevin Márquez
marquezberriosk@gmail.com

Author: Lewis Ochoa
lewis8a@gmail.com

This file contains the class GameOverState.
"""
import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.text import render_text

import settings


class EndState(BaseState):
    def enter(self, player, level) -> None:
        self.player = player
        self.level = level
        InputHandler.register_listener(self)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(settings.BASE_DIR / "sounds" / "music_end.mp3")
        pygame.mixer.music.play(loops=-1)

    def exit(self) -> None:
        InputHandler.unregister_listener(self)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.state_machine.change("start")

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 130, 196))

        render_text(
            surface,
            "Thanks for playing!",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            20,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

        self.y = 50

        for color, amount in self.player.coins_counter.items():
            surface.blit(
                settings.TEXTURES["tiles"],
                (settings.VIRTUAL_WIDTH // 2 - 32, self.y),
                settings.FRAMES["tiles"][color],
            )
            render_text(
                surface,
                "x",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2,
                self.y + 3,
                (255, 255, 255),
                shadowed=True,
            )
            render_text(
                surface,
                f"{amount}",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2 + 16,
                self.y + 3,
                (255, 255, 255),
                shadowed=True,
            )
            self.y += 20

        render_text(
            surface,
            f"Final Score: {self.player.score}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            self.y + 10,
            (255, 255, 255),
            shadowed=True,
            center=True,
        )

        render_text(
            surface,
            "Press Enter to start the adventure again!",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT - 20,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )
