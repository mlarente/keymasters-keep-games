from __future__ import annotations

from typing import List

from dataclasses import dataclass
import functools

from Options import OptionSet, Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ValkyriaChronicles4Options:
    valkyria_chonicles_4_enabled_dlc: ValkyriaChronicles4Dlc
    valkyria_chonicles_4_ranked_objectives: ValkyriaChronicles4RankedObjectives

def skirmishes(difficulty: str, n: int) -> List[str]:
    return [f"{difficulty} skirmish #{i}" for i in range(1, n + 1)]

class ValkyriaChronicles4(Game):
    name = "Valkyria Chronicles 4"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.XONE,
    ]
    is_adult_only_or_unrated = False
    options_cls = ValkyriaChronicles4Options

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            *self.battle_templates(self.story_battles, "story battle"),
            *self.battle_templates(self.squad_story_battles, "squad story battle"),
            *self.battle_templates(self.lower_skirmishes, weight_modifier=2),
            *self.battle_templates(self.higher_skirmishes, weight_modifier=2),
        ]
        if self.extra_story_battles:
            templates.extend(self.battle_templates(self.extra_story_battles, "extra story battle"))

        return templates

    def battle_templates(self, battles: List[str], battle_type="", weight_modifier=1) -> List[str]:
        battle = f'the {battle_type + ' "' if battle_type else ""}BATTLE{'"' if battle_type else ""}'
        ranked_modifier = self.archipelago_options.valkyria_chonicles_4_ranked_objectives.value

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

    story_battles = [
        "Prologue: Operation Northern Cross",
        "Chapter 1: The Battle of Fort Krest",
        "Chapter 2: The Liberation of Reine",
        "Interlude: Squad E Assembles",
        "Chapter 3: Rangers in the Storm (1)",
        "Chapter 3: Rangers in the Storm (2)",
        "Chapter 4: The Battle of Siegval (1)",
        "Chapter 4: The Battle of Siegval (2)",
        "Chapter 4: The Battle of Siegval (3)",
        "Chapter 5: Behind the Front Lines",
        "Chapter 6: The Point of No Return",
        "Chapter 7: A March in the Snow (1)",
        "Chapter 7: A March in the Snow (2)",
        "Interlude: The Other Kai",
        "Chapter 8: The Crystal Sea (1)",
        "Chapter 8: The Crystal Sea (2)",
        "Chapter 9: The Winter Witch",
        "Chapter 10: Under the Ice",
        "Chapter 11: The Sea Fortress",
        "Chapter 12: Midnight Run",
        "Chapter 13: Waiting for Springtime",
        "Chapter 14: Azure Flame",
        "Chapter 15: A Reason to Fight (1)",
        "Chapter 15: A Reason to Fight (2)",
        "Chapter 16: Forseti's Judgment",
        "Chapter 17: The Final Choice (1)",
        "Chapter 17: The Final Choice (2)",
        "Chapter 18: Devotion (1)",
        "Chapter 18: Devotion (2)",
    ]
    squad_story_battles = [
        "Like Old Times",
        "A Prayer for the Broken",
        "The Price of Skill",
        "Mischief Makers",
        "Reluctant Solitude",
        "Honor, Pride, and Regret",
        "Worlds Apart",
        "All the Single Ladies",
        "To Live Unbound",
        "Treading New Ground",
        "Legacies Left",
        "Girl in the Iron Mask",
        "Love and Logic",
        "Unfortunate Souls",
        "Gambler's Ruin",
        "Soul of the Navy",
        "A Chivalrous Heart",
    ]
    lower_skirmishes = skirmishes("normal", 10) + skirmishes("hard (*)", 9)

    @functools.cached_property
    def higher_skirmishes(self) -> List[str]:
        challenge_skirmishes = skirmishes("challenge (**)", 3)
        if "Expert Skirmishes" in self.enabled_dlc:
            return challenge_skirmishes + skirmishes("expert (***)", 6)
        return challenge_skirmishes

    @functools.cached_property
    def enabled_dlc(self) -> List[str]:
        return self.archipelago_options.valkyria_chonicles_4_enabled_dlc.value

    @functools.cached_property
    def extra_story_battles(self) -> List[str]:
        battles: List[str] = []

        battles_per_extra_story = {
            "A United Front with Squad 7": 3,
            "Squad E, to the Beach": 2,
            "A Captainless Squad": 3,
            "The Two Valkyria": 2,
            "Advance Ops": 1,
        }
        for dlc in battles_per_extra_story.keys():
            if dlc in self.enabled_dlc:
                if battles_per_extra_story[dlc] == 1:
                    battles.append(dlc)
                else:
                    battles.extend([
                        f'{dlc} ({i})'
                        for i in range(1, battles_per_extra_story[dlc] + 1)
                    ])

        return battles

class ValkyriaChronicles4Dlc(OptionSet):
    """
    DLC that may appear in objectives.

    Valid values:
    - A United Front with Squad 7
    - Squad E, to the Beach
    - A Captainless Squad
    - The Two Valkyria
    - Advance Ops
    - Expert Skirmishes
    """
    display_name = "Enabled DLC"
    valid_keys = [
        "A United Front with Squad 7",
        "Squad E, to the Beach",
        "A Captainless Squad",
        "The Two Valkyria",
        "Advance Ops",
        "Expert Skirmishes",
    ]
    default = valid_keys[:]

class ValkyriaChronicles4RankedObjectives(Range):
    """
    Odds needing an A rank in a battle, compared to just having to complete it.
    For example, 200 means that it's you're twice as likely to need an A rank than not.
    0 disables A rank objectives.
    """
    range_start = 0
    range_end = 200
    default = 100
    display_name = "Ranked objective odds"
