from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionError, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CatherineOptions:
    catherine_full_body_difficulties: CatherineDifficulties
    catherine_full_body_babel_stages: CatherineBabelStages

class Catherine(Game):
    name = "Catherine: Full Body"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]
    is_adult_only_or_unrated = False
    options_cls = CatherineOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Golden Playhouse: Reach the ENDING ending in MODE mode on DIFFICULTY difficulty",
                data={
                    "ENDING": (self.endings, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "MODE": (self.modes, 1),
                },
                is_time_consuming=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Golden Playhouse: Beat Rapunzel stage STAGE",
                data={
                    "STAGE": (lambda: [i for i in range(1, 16)], 1),
                },
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Golden Playhouse: Get at least RANK rank in the day DAY nightmare in MODE mode on DIFFICULTY difficulty",
                data={
                    "RANK": (self.ranks, 1),
                    "DAY": (lambda: [i for i in range(1, 11)], 1),
                    "MODE": (self.modes, 1),
                    "DIFFICULTY": (self.golden_playhouse_difficulties, 1),
                },
                weight=10
            ),
            GameObjectiveTemplate(
                label="Babel: Beat the BABEL_STAGE",
                data={
                    "BABEL_STAGE": (self.babel_stages, 1),
                },
                weight=5
            ),
        ]

    def difficulties(self) -> List[str]:
        difficulties = list(self.archipelago_options.catherine_full_body_difficulties.value)
        if not difficulties:
            raise OptionError("catherine_full_body_difficulties must have at least one value")
        return difficulties

    def babel_stages(self) -> List[str]:
        return list(self.archipelago_options.catherine_full_body_babel_stages.value)

    def golden_playhouse_difficulties(self) -> List[str]:
        difficulties = [d for d in self.difficulties() if d != "Safety"]
        if not difficulties:
            return ["Easy"]
        return difficulties

    def modes(self) -> List[str]:
        return ["Classic", "Remix"]

    def endings(self) -> List[str]:
        return [
            "Katherine True",
            "Katherine Good",
            "Katherine Bad",
            "Katherine Alternate",
            "Catherine True",
            "Catherine Good",
            "Catherine Bad",
            "Catherine Alternate",
            "Freedom True",
            "Freedom Good",
            "Rin True",
            "Rin Good",
            "Rin Normal",
        ]

    def ranks(self) -> List[str]:
        return ["Bronze", "Silver", "Gold"]

class CatherineDifficulties(OptionSet):
    """
    Difficulties that may be used in challenges.
    """
    display_name = "Allowed difficulties"
    valid_keys = [
        "Safety",
        "Easy",
        "Normal",
        "Hard",
    ]
    default = ["Easy", "Normal"]

class CatherineBabelStages(OptionSet):
    """
    Babel stages that may be used in challenges.
    """
    display_name = "Babel stages"
    valid_keys = [
        "Altar",
        "Menhir",
        "Obelisk",
        "Axis Mundi",
    ]
    default = [
        "Altar",
        "Menhir",
        "Obelisk",
    ]
