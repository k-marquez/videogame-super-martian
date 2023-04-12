"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

Author: Kevin Márquez
marquezberriosk@gmail.com

Author: Lewis Ochoa
lewis8a@gmail.com

This file contains the definition for items.
"""
from typing import Dict, Any

import random
from gale.timer import Timer

import settings
from src.GameItem import GameItem
from src.Player import Player
from src.states.entities.player_states import JumpState, WalkState, FallState


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
    settings.SOUNDS["key"].stop()
    settings.SOUNDS["key"].play()
    if(kwargs.get("level") <= settings.NUM_LEVELS):
        kwargs.get("state_machine").change("begind", level=kwargs.get("level"))
    else:
        kwargs.get("state_machine").change("end", player=player, level=kwargs.get("level"))

def hit_key_box_without_action(key_bloc: GameItem, player: Any):
    player.y = key_bloc.y - 18
    player.vy = player.vx = 0
    player.change_state("idle")

def hit_key_box_falling(key_bloc: GameItem, player: Any):
    player.vy = 0
    if player.x < key_bloc.x + 16 and key_bloc.x < player.x + player.width:
        player.y = key_bloc.y - 18
        if player.vx == 0:
            player.change_state("idle")
        elif player.vx > 0:
            player.change_state("walk", "right")
        else:
            player.change_state("walk", "left")

def hit_key_box_jumping(key_bloc: GameItem, player: Any, **enter_params: Dict[str,Any]):
    player.vy = 0
    player.y = key_bloc.y + player.height
    
    if not key_bloc.activate:
        key_bloc.activate = True
        settings.SOUNDS["box"].stop()
        settings.SOUNDS["box"].play()

        def arrive():
            key.collidable = True
        
        key = enter_params.get("item_key")
        key.in_play = True
        key.collidable = False
        final_y_key = key.y - 16
        Timer.tween(2, [ (key, {"y": final_y_key}) ], on_finish=arrive)

def hit_key_box_walking(key_bloc: GameItem, player: Any):
    player.vx = 0
    
    if player.x < key_bloc.x + 16:
        player.x = key_bloc.x + 17
    else:
        player.x = key_bloc.x - player.width - 1

def spawn_key(key_bloc: GameItem, player: Any, **enter_params: Dict[str,Any]):
    if isinstance(player.state_machine.current, JumpState):
        hit_key_box_jumping(key_bloc, player, **enter_params)
    elif isinstance(player.state_machine.current, WalkState):
        hit_key_box_walking(key_bloc, player)
    elif isinstance(player.state_machine.current, FallState):
        hit_key_box_falling(key_bloc, player)
    else:
        hit_key_box_without_action(key_bloc, player)
    
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
            "solidness": dict(top=True, right=True, bottom=True, left=True),
            "consumable": False,
            "collidable": True,
            "on_collide": spawn_key,
        }
    }
}
