from __future__ import annotations

from typing import List

from dataclasses import dataclass
import functools

from Options import OptionError, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class VoiceOfCardsOptions:
    voice_of_cards_included_games: VoiceofCardsIncludedGames

class VoiceOfCards(Game):
    name = "Voice of Cards"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PC,
    ]
    is_adult_only_or_unrated = False
    options_cls = VoiceOfCardsOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = []
        for game in self.included_games:
            templates.append(
                GameObjectiveTemplate(
                    label=f'{game} Multiplayer Game Parlor: win a game with "RULES" rules',
                    data={
                        "RULES": (self.rules, 1),
                    },
                    weight=10,
                )
            )
            templates.append(
                GameObjectiveTemplate(
                    label=f'{game} Multiplayer Game Parlor: trigger the skill of the CARD card',
                    data={
                        "CARD": (self.cards, 1),
                    },
                    weight=10,
                )
            )

        return templates

    rules = [
        "Simple",
        *["Add Skills"] * 3,
        *["Add Events"] * 7,
        *["Include All"] *10,
    ]
    cards = [
        "Ace",
        *(str(i) for i in range(2, 11)),
        "Jack",
        "Queen",
        "King",
    ]

    @functools.cached_property
    def included_games(self) -> List[str]:
        return self.archipelago_options.voice_of_cards_included_games.value


class VoiceofCardsIncludedGames(OptionSet):
    """
    Voice of Cards games that may be included in objectives.

    Valid values:
    - The Isle Dragon Roars
    - The Forsaken Maiden
    - The Beasts of Burden
    """
    display_name = "Included games"
    valid_keys = [
        "The Isle Dragon Roars",
        "The Forsaken Maiden",
        "The Beasts of Burden",
    ]
    default = valid_keys[:]

    def verify(self, *args, **kwargs):
        super().verify(*args, **kwargs)
        if not self.value:
            raise OptionError("You must include at least one game")
