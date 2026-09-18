from __future__ import annotations

from typing import List

from dataclasses import dataclass
import itertools

from Options import OptionError, OptionSet, Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CatherineOptions:
    catherine_full_body_difficulties: CatherineDifficulties
    catherine_full_body_babel_stages: CatherineBabelStages
    catherine_full_body_maximum_rapunzel_stage: CatherineMaximumRapunzelStage
    catherine_full_body_maximum_rapunzel_extra_stage: CatherineMaximumRapunzelExtraStage

class Catherine(Game):
    name = "Catherine: Full Body"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]
    is_adult_only_or_unrated = False
    options_cls = CatherineOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
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
        ]
        if self.self.golden_playhouse_difficulties():
            templates.append(GameObjectiveTemplate(
                label="Golden Playhouse: Get at least RANK rank in the day DAY nightmare in MODE mode on DIFFICULTY difficulty",
                data={
                    "RANK": (self.ranks, 1),
                    "DAY": (lambda: [i for i in range(1, 11)], 1),
                    "MODE": (self.modes, 1),
                    "DIFFICULTY": (self.golden_playhouse_difficulties, 1),
                },
                weight=10
            ))
        if self.babel_stages():
            templates.append(GameObjectiveTemplate(
                label="Babel: Beat the BABEL_STAGE",
                data={
                    "BABEL_STAGE": (self.babel_stages, 1),
                },
                weight=5
            ))
        if self.rapunzel_stages():
            templates.append(GameObjectiveTemplate(
                label="Golden Playhouse: Beat Rapunzel STAGE",
                data={
                    "STAGE": (self.rapunzel_stages, 1),
                },
                weight=7,
            ))

        return templates

    def difficulties(self) -> List[str]:
        difficulties = list(self.archipelago_options.catherine_full_body_difficulties.value)
        if not difficulties:
            raise OptionError("catherine_full_body_difficulties must have at least one value")
        return difficulties

    def babel_stages(self) -> List[str]:
        return list(self.archipelago_options.catherine_full_body_babel_stages.value)

    def golden_playhouse_difficulties(self) -> List[str]:
        return list(d for d in self.difficulties() if d != "Safety")

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

    def rapunzel_stages(self) -> List[str]:
        max_stage = self.archipelago_options.catherine_full_body_maximum_rapunzel_stage.value
        max_extra_stage = self.archipelago_options.catherine_full_body_maximum_rapunzel_extra_stage.value

        return list(itertools.chain(
            (f"stage {i}" for i in range(1, max_stage + 1)),
            (f"extra stage {i}" for i in range(1, max_extra_stage + 1)),
        ))

class CatherineDifficulties(OptionSet):
    """
    Difficulties that may be used in objectives.

    Valid values:
    - Safety
    - Easy
    - Normal
    - Hard

    Note that enabling only Safety will disable nightmare objectives.
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
    Babel stages that may be used in objectives.
    Use an empty list to disable Babel stage objectives.

    Valid values:
    - Altar
    - Menhir
    - Obelisk
    - Axis Mundi
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

class CatherineMaximumRapunzelStage(Range):
    """
    Highest Rapunzel stage that may be included in objectives.
    Set to zero to disable Rapunzel stage objectives.
    """
    range_end = 64
    default = 15

class CatherineMaximumRapunzelExtraStage(Range):
    """
    Highest Rapunzel extra stage that may be included in objectives.
    Set to zero to disable Rapunzel extra stage objectives.
    """
    range_end = 64
