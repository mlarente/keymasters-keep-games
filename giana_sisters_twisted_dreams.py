from __future__ import annotations

from typing import List

from dataclasses import dataclass
import functools

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


def level_names(world: int, num_levels: int) -> List[str]:
    return list(f"{world}-{i}" for i in range(1, num_levels + 1))

@dataclass
class GianaSistersOptions:
    giana_sisters_twisted_dreams_include_rise_of_the_owlverlord: GianaSistersIncludeRiseOfTheOwlverlord
    giana_sisters_twisted_dreams_include_special_levels: GianaSistersIncludeSpecialLevels

class GianaSisters(Game):
    name = "Giana Sisters: Twisted Dreams"
    platform = KeymastersKeepGamePlatforms.PC
    platforms_other = [
        KeymastersKeepGamePlatforms.X360,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.WIIU,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.SW,
    ]
    is_adult_only_or_unrated = False
    options_cls = GianaSistersOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete the LEVEL level",
                data={
                    "LEVEL": (self.all_levels, 1),
                },
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Get 5 stars in the LEVEL level (hard mode)",
                data={
                    "LEVEL": (self.star_levels, 1),
                },
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Complete the LEVEL level and find all the big gems",
                data={
                    "LEVEL": (self.big_gems_levels, 1),
                },
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Complete the LEVEL level in hardcore mode",
                data={
                    "LEVEL": (self.star_levels, 1),
                },
                is_difficult=True,
                weight=5,
            ),
        ]

        return templates

    world_1_levels = level_names(1, 7)
    world_2_levels = level_names(2, 8)
    world_3_levels = level_names(3, 11)
    base_levels = world_1_levels + world_2_levels + world_3_levels
    rise_of_the_owlverlord_levels = level_names(4, 7)
    special_levels = [
        "Halloween special 2012",
        "Christmas special 2012",
        "Halloween special 2013 - normal",
        "Halloween special 2013 - hard",
        "Christmas special 2013",
    ]

    @property
    def include_rise_of_the_owlverlord(self) -> bool:
        return self.archipelago_options.giana_sisters_twisted_dreams_include_rise_of_the_owlverlord.value

    @property
    def include_special_levels(self) -> bool:
        return self.archipelago_options.giana_sisters_twisted_dreams_include_special_levels.value

    @functools.cached_property
    def all_levels(self) -> List[str]:
        levels = self.base_levels[:]
        if self.include_rise_of_the_owlverlord:
            levels.extend(self.rise_of_the_owlverlord_levels)
        if self.include_special_levels:
            levels.extend(self.special_levels)
        return levels

    @functools.cached_property
    def star_levels(self) -> List[str]:
        levels = self.base_levels[:]
        if self.include_rise_of_the_owlverlord:
            levels.extend(self.rise_of_the_owlverlord_levels)
        return levels

    @functools.cached_property
    def big_gems_levels(self) -> List[str]:
        levels = self.world_1_levels[:-1] + self.world_2_levels[:-1] + self.world_3_levels[:-1]
        if self.include_rise_of_the_owlverlord:
            levels.extend(self.rise_of_the_owlverlord_levels)
        if self.include_special_levels:
            levels.extend(self.special_levels)
        return levels

class GianaSistersIncludeRiseOfTheOwlverlord(DefaultOnToggle):
    """
    Include Rise of the Owlverlord content.
    """
    display_name = "Include Rise of the Owlverlord"

class GianaSistersIncludeSpecialLevels(DefaultOnToggle):
    """
    Include the Halloween and Christmas special levels.
    """
    display_name = "Include special levels"
