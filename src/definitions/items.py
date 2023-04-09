"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

Edit by: Kevin Márquez
marquezberriosk@gmail.com

This file contains the definition for items.
"""
from typing import Dict, Any
import pudb

import random

from gale.timer import Timer

import settings
from src.GameItem import GameItem
from src.Player import Player


def pickup_coin(
    coin: GameItem, player: Player, points: int, color: int, time: float
) -> None:
    settings.SOUNDS["pickup_coin"].stop()
    settings.SOUNDS["pickup_coin"].play()
    player.score += points
    player.coins_counter[color] += 1
    Timer.after(time, lambda: coin.respawn())


def pickup_green_coin(coin: GameItem, player: Player, **kwargs: Dict[str,Any]):
    pickup_coin(coin, player, 1, 62, random.uniform(2, 4))


def pickup_blue_coin(coin: GameItem, player: Player, **kwargs: Dict[str,Any]):
    pickup_coin(coin, player, 5, 61, random.uniform(5, 8))


def pickup_red_coin(coin: GameItem, player: Player, **kwargs: Dict[str,Any]):
    pickup_coin(coin, player, 20, 55, random.uniform(10, 18))


def pickup_yellow_coin(coin: GameItem, player: Player, **kwargs: Dict[str,Any]):
    pickup_coin(coin, player, 50, 54, random.uniform(20, 25))
    
def pickup_key(key: GameItem, player: Player, **kwargs: Dict[str,Any]):
    kwargs.get("state_machine").change("play", score = player.score, level = kwargs.get("level"))

def spawn_key(key_bloc: GameItem, another: Any, **enter_params: Dict[str,Any]):
    if not key_bloc.activate:
        key_bloc.activate = True

        def arrive():
            key.collidable = True
        
        key = enter_params.get("item_key")
        key.in_play = True
        key.collidable = False
        final_y_key = key.y - 16
        Timer.tween(2, [ (key, {"y": final_y_key}) ], on_finish=arrive)
    
ITEMS: Dict[str, Dict[int, Dict[str, Any]]] = {
    "coins": {
        62: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_green_coin,
        },
        61: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_blue_coin,
        },
        55: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_red_coin,
        },
        54: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_yellow_coin,
        },
    },
    "key": {
        56: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_key,
        }
    },
    "key_block": {
        49: {
            "texture_id": "tiles",
            "solidness": dict(top=True, right=False, bottom=True, left=False),
            "consumable": False,
            "collidable": True,
            "on_collide": spawn_key,
        }
    }
}
