from __future__ import annotations

from typing import List

from dataclasses import dataclass
import functools

from Options import Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Doa6Options:
    doa6_combo_training_requirement: Doa6ComboTrainingRequirement
    doa6_command_training_requirement: Doa6CommandTrainingRequirement
    doa6_combo_challenge_requirement: Doa6ComboChallengeRequirement
    doa6_minimum_difficulty: Doa6MinimumDifficulty
    doa6_maximum_difficulty: Doa6MaximumDifficulty

class Doa6(Game):
    name = "Dead or Alive 6"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.ARC,
    ]
    is_adult_only_or_unrated = False
    options_cls = Doa6Options

    def training_objective_template(self, training_type: str, percent_requirement: int) -> GameObjectiveTemplate:
        if percent_requirement == 100:
            label = f"Complete {training_type} training as CHARACTER"
        else:
            label = f"Complete at least {percent_requirement}% of {training_type} training as CHARACTER"

        return GameObjectiveTemplate(
            label=label,
            data={"CHARACTER": (self.characters, 1)},
            weight=2,
        )

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        combo_challenge_requirement = self.archipelago_options.doa6_combo_challenge_requirement.value

        return [
            self.training_objective_template('Combo', self.archipelago_options.doa6_combo_training_requirement.value),
            self.training_objective_template('Command', self.archipelago_options.doa6_command_training_requirement.value),
            GameObjectiveTemplate(
                label="Complete Combo challenge as CHARACTER"
                    if combo_challenge_requirement == 100
                    else f"Complete at least {combo_challenge_requirement}/20 of Combo challenge as CHARACTER",
                data={
                    "CHARACTER": (self.player_characters, 1),
                },
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete Arcade mode on DIFFICULTY difficulty as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Complete Time attack mode on DIFFICULTY difficulty as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Attempt Survival mode on DIFFICULTY difficulty as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Land a SPECIAL_MOVE against a DIFFICULTY difficulty OPPONENT QTY times as CHARACTER",
                data={
                    "SPECIAL_MOVE": (self.special_moves, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "OPPONENT": (self.characters, 1),
                    "QTY": ([5, 10, 15], 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win QTY Versus matches (ROUNDS) as CHARACTER against a DIFFICULTY difficulty OPPONENT in STAGE",
                data={
                    "QTY": (self.versus_wins, 1),
                    "ROUNDS": (self.rounds, 1),
                    "CHARACTER": (self.player_characters, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "OPPONENT": (self.characters, 1),
                    "STAGE": (self.stages, 1),
                },
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win DIFFICULTY difficulty Versus matches (ROUNDS) as CHARACTER in STAGE against: OPPONENTS",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "ROUNDS": (self.rounds, 1),
                    "CHARACTER": (self.player_characters, 1),
                    "OPPONENTS": (self.characters, self.versus_wins),
                    "STAGE": (self.stages, 1),
                },
                weight=8,
            ),
        ]

    versus_wins = [3, 5, 8]

    characters = [
        "Kasumi",
        "Helena",
        "Hayate",
        "Hayabusa",
        "Jann Lee",
        "Zack",
        "Diego",
        "Rig",
        "Hitomi",
        "Leifang",
        "Ayane",
        "Marie Rose",
        "Honoka",
        "Bayman",
        "Bass",
        "Tina",
        "Mila",
        "Christie",
        "NiCO",
        "Kokoro",
        "La Mariposa",
        "Brad Wong",
        "Eliot",
        "Nyotengu",
        "Phase 4",
        "Raidou",
        "Momiji",
        "Rachel",
        "Tamaki",
        "Mai",
        "Kula",
    ]

    player_characters = [*characters, "any fighter"]

    @functools.cached_property
    def difficulties(self) -> List[str]:
        values = (
            self.archipelago_options.doa6_minimum_difficulty.value,
            self.archipelago_options.doa6_maximum_difficulty.value,
        )

        return [f"{d} ({i + 1})" for i, d in enumerate([
            "Rookie",
            "Easy",
            "Normal",
            "Hard",
            "Champ",
            "True Fighter",
            "Master",
            "Legend",
        ])][min(*values) - 1:max(*values)]

    special_moves = [
        "Break Blow",
        "Break Hold",
    ]
    rounds = [f"{n} round{"s" if n > 1 else ""}" for n in range(1,6)]
    stages = [
        "Forbidden Fortune",
        "Lost Paradise",
        "Unforgettable",
        "DOA Colosseum",
        "Road Rage",
        "Chinese Festival",
        "Zero",
        "A.P.O.",
        "The Throwdown",
        "Miyabi",
        "Hidden Garden",
        "The Muscle",
        "Sweat",
        "Seaside Eden",
    ]

class Doa6TrainingRequirement(Range):
    range_start = 10
    range_end = 100
    default = 90

class Doa6ComboTrainingRequirement(Doa6TrainingRequirement):
    """
    Percentage of the combo training to complete for a combo training objective.
    """

class Doa6CommandTrainingRequirement(Doa6TrainingRequirement):
    """
    Percentage of the command training to complete for a command training objective.
    """

class Doa6ComboChallengeRequirement(Range):
    """
    Number of combos required for the combo challenge objectives.
    """
    range_start = 5
    range_end = 20
    default = 15

class Doa6Difficulty(Range):
    range_start = 1
    range_end = 8

class Doa6MinimumDifficulty(Doa6Difficulty):
    """
    Minimum difficulty that may be required in objectives.
    """
    default = 4

class Doa6MaximumDifficulty(Doa6Difficulty):
    """
    Maximum difficulty that may be required in objectives.
    """
    default = 6
