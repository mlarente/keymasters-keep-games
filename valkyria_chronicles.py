from __future__ import annotations

from typing import List

from dataclasses import dataclass
import functools

from Options import OptionSet, Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ValkyriaChroniclesOptions:
    valkyria_chonicles_enabled_dlc: ValkyriaChroniclesDlc
    valkyria_chonicles_ranked_objectives: ValkyriaChroniclesRankedObjectives

def skirmishes(difficulty: str, n: int) -> List[str]:
    return [f"{difficulty} skirmish #{i}" for i in range(1, n + 1)]

class ValkyriaChronicles(Game):
    name = "Valkyria Chronicles"
    platform = KeymastersKeepGamePlatforms.PS3
    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
    ]
    is_adult_only_or_unrated = False
    options_cls = ValkyriaChroniclesOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            *self.battle_templates(self.story_battles, "story battle"),
            *self.battle_templates(self.all_skirmishes, weight_modifier=2),
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

    @functools.cached_property
    def story_battles(self) -> List[str]:
        battles = [
            "Prologue: Gallia, to Arms!",
            "Chapter 1: In Defense of Bruhl",
            "Chapter 2: Escape from Bruhl",
            "Chapter 3: Vasel Urban Warfare",
            "Chapter 4: Operation Cloudburst",
            "Chapter 5: The Wooden Wildwood",
            "Chapter 6: A Desert Encounter",
            "Chapter 7: The Battle at Barious",
            # [...]
            "Report: Largo's Passion",
        ]
        if "Enter the Edy Detachement" in self.enabled_dlc:
            battles.append("Enter the Edy Detachement (DLC)")
        return battles

    edy_detachment_skirmishes = [
        "Scout Trial",
        "Lancer Trial",
        "Sniper Trial",
        "Engineer Trial",
        "Shock trooper Trial",
        "Tank Trial",
    ]

    @functools.cached_property
    def all_skirmishes(self) -> List[str]:
        battles = [s for d in ["easy", "normal", "hard"] for s in skirmishes(d, 9)]
        if "Hard EX mode" in self.enabled_dlc:
            battles.extend(skirmishes("expert", 9))
        if "Challenge of the Edy Detachement" in self.enabled_dlc:
            battles.extend(f"{s} skirmish" for s in self.edy_detachment_skirmishes)
        if "Behind Her Blue Flame" in self.enabled_dlc:
            battles.append('DLC story "Behind Her Blue Flame" (3 battles)')
        return battles

    @functools.cached_property
    def enabled_dlc(self) -> List[str]:
        return self.archipelago_options.valkyria_chonicles_enabled_dlc.value

class ValkyriaChroniclesDlc(OptionSet):
    """
    DLC that may appear in objectives.

    Valid values:
    - Enter the Edy Detachement
    - Challenge of the Edy Detachement
    - Hard EX mode
    - Behind Her Blue Flame
    """
    display_name = "Enabled DLC"
    valid_keys = [
        "Enter the Edy Detachement",
        "Challenge of the Edy Detachement",
        "Hard EX mode",
        "Behind Her Blue Flame",
    ]
    default = [
        "Enter the Edy Detachement",
        "Challenge of the Edy Detachement",
    ]

class ValkyriaChroniclesRankedObjectives(Range):
    """
    Odds needing an A rank in a battle, compared to just having to complete it.
    For example, 200 means that it's you're twice as likely to need an A rank than not.
    0 disables A rank objectives.
    """
    range_start = 0
    range_end = 200
    default = 100
    display_name = "Ranked objective odds"
