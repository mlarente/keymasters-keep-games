from __future__ import annotations

from typing import Dict, List, Tuple

from dataclasses import dataclass
import functools
import math

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

class Battle:
    def __init__(self, type: str, name: str, lvl: int, free_deployment_slots: int, must_deploy: List[str] = [], cant_deploy: List[str] = []):
        self.type = type
        self.name = name
        self.lvl = lvl
        self.free_deployment_slots = free_deployment_slots
        self.must_deploy = must_deploy
        self.cant_deploy = cant_deploy

    @functools.cached_property
    def label(self):
        type_labels = {"mock": "Mental Mock", "story": "Story"}
        return f"{type_labels[self.type]} Battle: Complete {self.name}"

all_battles = [
    Battle("mock", "Basic Training", 3, 6),
    Battle("mock", "Pincer Attack", 3, 6),
    Battle("mock", "Combating Mages", 4, 6),
    Battle("mock", "A Fair Fight", 6, 8),
    Battle("mock", "A Speedy Victory", 8, 10),
    Battle("mock", "Close Quarters Combat", 10, 9),
    Battle("mock", "A Battle Under Three Flags", 11, 10),
    Battle("mock", "Take Back the Boat", 13, 12),
    Battle("mock", "To the Last Man", 15, 12),
    Battle("mock", "Defend the Arena", 17, 10),
    Battle("mock", "The Chaos of Battle", 18, 12),
    Battle("mock", "Forces Divided", 20, 11, ["Serenoa"]),
    Battle("mock", "Take Back the Castle Gate", 21, 9, ["Serenoa"]),
    Battle("mock", "Conquer the Arena", 23, 10),
    Battle("mock", "A Desperate Assault", 25, 12),
    Battle("mock", "Field of Greed", 27, 12),
    Battle("mock", "Mine Cart Tactics", 30, 10),
    Battle("mock", "Seize the Dais", 32, 8),
    Battle("mock", "Last Man Standing", 33, 10),
    Battle("mock", "A Battle of Wits", 33, 9, ["Serenoa"]),
    Battle("mock", "Guerilla Tactics", 33, 10),
    Battle("mock", "A Swift Escape", 34, 9, ["Serenoa"]),
    Battle("mock", "No Soldier Left Behind", 35, 10),
    Battle("mock", "Against the Storm", 37, 10),
    Battle("mock", "To Each Their Own", 39, 10),
    Battle("mock", "Turning the Tides", 41, 8),
    Battle("mock", "Fort Assault", 43, 10),
    Battle("mock", "Crimson Fields", 45, 10),
    Battle("mock", "An Ally in Need", 47, 9, ["Frederica"]),
    Battle("mock", "Conquering the Carts", 49, 10),
    Battle("mock", "Lift Off", 50, 9, ["Serenoa"]),
    Battle("mock", "Under the Iron Gate", 50, 12),
    Battle("mock", "Before the Goddess", 50, 12),
    Battle("mock", "A Long Trek", 50, 12),
    Battle("mock", "The Assassins", 50, 12),
    Battle("story", "Beset by Brigands", 50, 0, ["Serenoa", "Benedict", "Frederica", "Geela", "Roland"]),
    Battle("story", "The Tourney", 50, 6, ["Serenoa", "Roland"], ["Cordelia"]),
    Battle("story", "Subduing the Smugglers", 50, 6, ["Serenoa", "Rudolph"]),
    Battle("story", "Apprehending the Rebels", 50, 6, ["Serenoa", "Corentin"]),
    Battle("story", "Defending Dragan", 50, 8, ["Serenoa"]),
    Battle("story", "Storming the Whiteholm Castle Gardens", 50, 7, ["Serenoa", "Roland"]),
    Battle("story", "Escape from Whiteholm Castle", 50, 7, ["Serenoa", "Roland"], ["Maxwell"]),
    Battle("story", "General Avlora's Assault", 50, 9, ["Serenoa"], ["Avlora"]),
    Battle("story", "Landroi's Last Stand", 50, 9, ["Serenoa"], ["Roland"]),
    Battle("story", "Betrayed Beneath the Tellioran Moon", 50, 8, ["Serenoa", "Roland"]),
    Battle("story", "House Telliore's Treachery", 50, 9, ["Serenoa"]),
    Battle("story", "House Ende's Assault", 50, 8, ["Serenoa"], ["Roland", "Avlora"]),
    Battle("story", "Attack on Avlora", 50, 8, ["Serenoa"], ["Roland", "Avlora"]),
    Battle("story", "A Rematch with Bandits", 50, 9, ["Serenoa"], ["Travis", "Trish"]),
    Battle("story", "The Battle of Booker's Brigade", 50, 9, ["Sorenoa"]),
    Battle("story", "Clash with Sycras", 50, 9, ["Serenoa"]),
    Battle("story", "A Battle with the Herosbane", 50, 5, ["Serenoa", "Roland"]),
    Battle("story", "The Battle of House Ende", 50, 8, ["Serenoa", "Benedict"]),
    Battle("story", "A Decisive Duel", 50, 6, ["Serenoa"]),
    Battle("story", "Routing the Roselle", 50, 9, ["Serenoa"]),
    Battle("story", "Safeguarding the Roselle", 50, 9, ["Serenoa"]),
    Battle("story", "Confronting Silvio", 50, 9, ["Serenoa"]),
    Battle("story", "Securing Telliore Reservoir", 50, 9, ["Serenoa", "Milo"]),
    Battle("story", "Securing the Warship", 50, 9, ["Serenoa", "Milo"]),
    Battle("story", "Securing Whiteholm Bridge", 50, 9, ["Serenoa", "Milo"]),
    Battle("story", "Battle Upon the Bridge", 50, 8, ["Serenoa", "Roland", "Milo"]),
    Battle("story", "Clash Within Whiteholm Castle", 50, 8, ["Serenoa", "Roland", "Milo"], ["Avlora"]),
    Battle("story", "Skirmish on the Norzelia River", 50, 9, ["Serenoa", "Milo"], ["Avlora"]),
    Battle("story", "Patriatte's Gambit", 50, 8, ["Serenoa", "Milo"], ["Roland", "Frederica"]),
    Battle("story", "Routing the Royalists", 50, 7, ["Serenoa", "Roland", "Cordelia"], ["Benedict", "Frederica"]),
    Battle("story", "Battle with the Bandit Travis", 50, 9, ["Serenoa"], ["Roland", "Benedict", "Travis"]),
    Battle("story", "Battle with the Bandit Trish", 50, 9, ["Serenoa"], ["Roland", "Benedict", "Trish"]),
    Battle("story", "Eliminating the Aesfrosti Soldiers", 50, 9, ["Serenoa"]),
    Battle("story", "Confronting Clarus", 50, 9, ["Serenoa"], ["Roland"]),
    Battle("story", "Battle of Twinsgate", 50, 9, ["Serenoa"], ["Frederica"]),
    Battle("story", "Battle at the Ministry", 50, 9, ["Serenoa"], ["Benedict"]),
    Battle("story", "Benedict's Battle", 50, 9, ["Benedict"], ["Roland", "Frederica"]),
    Battle("story", "Roland's Battle", 50, 9, ["Roland"], ["Benedict", "Frederica"]),
    Battle("story", "Frederica's Battle", 50, 9, ["Frederica"], ["Benedict", "Roland"]),
    Battle("story", "The End of Exharme", 50, 9, ["Serenoa"], ["Roland"]),
    Battle("story", "Defeating the Archduke", 50, 9, ["Serenoa"], ["Frederica"]),
    Battle("story", "Flight from the Source", 50, 8, ["Serenoa", "Frederica"], ["Benedict"]),
    Battle("story", "Piercing the Goddess's Shield", 50, 9, ["Serenoa"]),
    Battle("story", "The Holy Automaton", 50, 9, ["Serenoa"], ["Roland"]),
    Battle("story", "Battling the Embittered Svarog", 50, 9, ["Serenoa"], ["Frederica"]),
    Battle("story", "Fighting Idore the Deluded", 50, 9, ["Serenoa"], ["Benedict"]),
    Battle("story", "Fighting Lyla Visecraft", 50, 9, ["Serenoa"]),
    Battle("story", "The Final Battle", 50, 9, ["Serenoa"]),
]

all_characters = [
    "Serenoa",
    "Roland",
    "Benedict",
    "Frederica",
    "Geela",
    "Anna",
    "Hughette",
    "Erador",
    "Rudolph",
    "Corentin",
    "Julio",
    "Milo",
    "Cordelia",
    "Travis",
    "Trish",
    "Avlora",
    "Hossabara",
    "Narve",
    "Medina",
    "Jens",
    "Maxwell",
    "Archibald",
    "Flanagan",
    "Ezana",
    "Lionel",
    "Groma",
    "Piccoletta",
    "Decimal",
    "Quahaug",
    "Giovanna",
]

@dataclass
class NoOptions:
    pass

class TriangleStrategy(Game):
    name = "Triangle Strategy"
    platform = KeymastersKeepGamePlatforms.SW
    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]
    is_adult_only_or_unrated = False
    options_cls = NoOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        all_battle_labels = [b.label for b in all_battles]
        templates = [
            GameObjectiveTemplate(
                label='BATTLE',
                data={
                    "BATTLE": (all_battle_labels, 1),
                },
                weight=len(all_battle_labels),
            )
        ]
        for (slots, unavailable_characters), battles in self.per_deployments(all_battles):
            forced_slots = math.ceil(slots / 2)
            if forced_slots:
                templates.append(GameObjectiveTemplate(
                    label='BATTLE with CHARACTERS deployed',
                    data={
                        "BATTLE": ([b.label for b in battles], 1),
                        "CHARACTERS": ([c for c in all_characters if c not in unavailable_characters], forced_slots),
                    },
                    weight=len(battles),
                ))

        return templates

    def per_deployments(self, battles: List[Battle]) -> List[Tuple[Tuple[int, List[str]], List[Battle]]]:
        def deployment_string(battle: Battle):
            return f"{battle.free_deployment_slots}-{",".join(sorted(battle.must_deploy + battle.cant_deploy))}"

        per_dep_battles: Dict[str, List[Battle]] = {}
        for battle in battles:
            s = deployment_string(battle)
            if s not in per_dep_battles:
                per_dep_battles[s] = []
            per_dep_battles[s].append(battle)

        return [
            (
                (battles[0].free_deployment_slots, sorted(battles[0].must_deploy + battles[0].cant_deploy)),
                battles,
            ) for battles in per_dep_battles.values()
        ]

    def battle_templates(self, battles: List[str], battle_type="", weight_modifier=1) -> List[str]:
        battle = f'the {battle_type + ' "' if battle_type else ""}BATTLE{'"' if battle_type else ""}'
        ranked_modifier = self.archipelago_options.valkyria_chonicles_ranked_objectives.value

        return [
            GameObjectiveTemplate(
                label=f'Complete {battle}',
                data={
                    "BATTLE": (battles, 1),
                },
                weight=len(battles) * 100 // weight_modifier,
            ),
            GameObjectiveTemplate(
                label=f'Achieve A-rank in the {battle}',
                data={
                    "BATTLE": (battles, 1),
                },
                weight=len(battles) * ranked_modifier // weight_modifier,
            ),
        ]
