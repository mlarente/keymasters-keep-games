from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class NoOptions:
    pass

class KazeAndTheWildMasks(Game):
    name = "Kaze and the Wild Masks"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.PC,
    ]
    is_adult_only_or_unrated = False
    options_cls = NoOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label=f'In {world}, complete LEVEL',
                data={
                    "LEVEL": (self.levels[world], 1),
                },
                weight=10,
            )
            for world in self.levels.keys()
        ]

    levels = {
        "Forgotten Grove": [
            "Cranky Carrots",
            "Jelly Jungle",
            "Watch Your Step",
            "Thorny Tree",
            "Vine Climb",
            "Lights On Lights Off",
            "Bean Bay",
            "Mother Mona",
        ],
        "Frozen Mountain": [
            "Sliding Salad",
            "Slingshot Ride",
            "Beets and Bounces",
            "Tiger Popsicle",
            "Ropes of Hope",
            "Arctic Blizzard",
            "Forgotten Mask",
            "Pumpkin Pyre",
            "Buck's Brigade",
        ],
        "Toxic Tide": [
            "Feel the Flow",
            "Zipline Zipvine",
            "Scales Showdown",
            "Free Fall",
            "Gusty Cliffs",
            "Toxic Lake",
            "Ride to Heaven",
            "Sprint of Spirits",
            "Olaf's Lair",
        ],
        "Carrotland": [
            "Volcanic Star",
            "Hurry Hurricane",
            "Jelly Dungeon",
            "Ziplizard",
            "Haunted Lake",
            "Circuit Capers",
            "Scalding Gears",
            "Bulletvator",
            "Typhoon's Tussle",
        ],
    }
