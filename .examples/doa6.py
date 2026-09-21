# Example of a Keymaster's Keep game implementation
#
# This should be saved as `name_of_the_game.py` in the `keymasters_keep` folder of your Archipelago installation.
# Once it's there, you can generate the YAML templates and the game will be added to the `game_selection` option of the
# template.
#
# As in YAML, comments start with a `#`, indentation is important but newlines are not.

from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MyOptions:
    pass

class MyGame(Game):
    # Name of the game, as displayed by KMK
    name = "Dead or Alive 6"

    # Main platform of the game.
    # Possible values: https://github.com/silasary/Archipelago/blob/keymasters_keep/worlds/keymasters_keep/enums.py#L4
    platform = KeymastersKeepGamePlatforms.PS4
    # Other platforms. May be empty if there's only one platform.
    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.ARC,
    ]

    is_adult_only_or_unrated = False
    options_cls = MyOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            # Each GameObjectiveTemplate is a possible kind objective.
            GameObjectiveTemplate(

                # Sentence template of the objective
                label="Complete TRAINING_TYPE training (at least 90%) as CHARACTER",

                # Datasets for this template.
                # KMK will look for each key (in this case TRAINING_TYPE and CHARACTER) in the label and replace them
                # with a value (or multiple values) from the corresponding dataset.
                data={
                    # This means: replace `TRAINING_TYPE` in the label with one (the "1" at the end) of the values in
                    # `training_types` (defined further down).
                    "TRAINING_TYPE": (self.training_types, 1),
                    "CHARACTER": (self.characters, 1),
                },

                # Optional. Can be set to `True` instead of `False` to indicate time consuming or difficult challenges.
                is_time_consuming=False,
                is_difficult=False,

                # Odds that this template will be used, compared to the other templates in this list.
                # Defaults to 1 if not set.
                weight=3,
            ),

            GameObjectiveTemplate(
                label="Complete Combo challenge (at least 15/20) as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                weight=3,
            ),

            GameObjectiveTemplate(
                label="Complete Arcade mode on DIFFICULTY difficulty as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.characters, 1),
                },
                weight=10,
            ),

            GameObjectiveTemplate(
                label="Complete Time attack mode on DIFFICULTY difficulty as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.characters, 1),
                },
                weight=8,
            ),

            GameObjectiveTemplate(
                label="Attempt Survival mode on DIFFICULTY difficulty as CHARACTER",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.characters, 1),
                },
                weight=5,
            ),

            GameObjectiveTemplate(
                label="Land a SPECIAL_MOVE against a DIFFICULTY difficulty OPPONENT QTY times as CHARACTER",
                data={
                    "SPECIAL_MOVE": (self.special_moves, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "OPPONENT": (self.characters, 1),
                    "QTY": (self.special_move_quantities, 1),
                    "CHARACTER": (self.characters, 1),
                },
                weight=5,
            ),

            GameObjectiveTemplate(
                label="Win QTY Versus matches (ROUNDS rounds) as CHARACTER against a DIFFICULTY difficulty OPPONENT in STAGE",
                data={
                    "QTY": (self.versus_wins_quantities, 1),
                    "ROUNDS": (self.rounds, 1),
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "OPPONENT": (self.characters, 1),
                    "STAGE": (self.stages, 1),
                },
                weight=8,
            ),

            GameObjectiveTemplate(
                label="Win DIFFICULTY difficulty Versus matches (ROUNDS rounds) as CHARACTER against a OPPONENTS in STAGE",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "ROUNDS": (self.rounds, 1),
                    "CHARACTER": (self.characters, 1),

                    # The number of selected values can be random as well.
                    # Here we use one of the numbers in `versus_opponent_quantities` (defined further down) to select
                    # multiple opponents.
                    "OPPONENTS": (self.characters, self.versus_opponent_quantities),

                    "STAGE": (self.stages, 1),
                },
                weight=8,
            ),
        ]

    # Dataset referenced in objective templates. Should be alist of strings.
    # Each value as an equal chance of being picked. You can repeat values to increase the odds of getting one value.
    # It can also be done like this:
    # my_data_set = [
    #     "One-time value",
    #     *["This value is added four times"] * 4,
    # ]
    #
    # Different types of quotes may be used. All of these are valid:
    # "double quotes (may contain 'single quote' without issues)"
    # 'single quote (may contain "double quotes" without issues)'
    # """triple double quotes (may contain "double quotes" and 'single quotes' without issues)"""
    # '''triple single quotes (may contain "double quotes" and 'single quotes' without issues)'''
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

    training_types = [
        "Command",
        "Combo",
    ]

    difficulties = [
        "Rookie (1)",
        "Easy (2)",
        "Normal (3)",
        "Hard (4)",
        "Champ (5)",
        "True Fighter (6)",
        "Master (7)",
        "Legend (8)",
    ]

    special_moves = [
        "Break Blow",
        "Break Hold",
    ]

    special_move_quantities = [
        "5",
        "10",
        "15",
    ]

    versus_wins_quantities = [
        "3",
        "5",
        "8",
    ]

    rounds = [
        "1",
        "2",
        "3",
        "4",
        "5",
    ]

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

    # This one is used to determine a number of selected value,
    # therefore it has to be integers instead of strings (no quotes).
    versus_opponent_quantities = [
        3,
        5,
        8,
    ]
