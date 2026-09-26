from __future__ import annotations

from typing import List

from dataclasses import dataclass
import functools

from Options import DefaultOnToggle, OptionError, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class NinjaGaidenOptions:
    ninja_gaiden_master_collection_include_ng2: IncludeNinjaGaiden2
    ninja_gaiden_master_collection_ng2_chapter_difficulties: NinjaGaiden2ChapterDifficulties
    ninja_gaiden_master_collection_ng2_mission_difficulties: NinjaGaiden2MissionDifficulties

    ninja_gaiden_master_collection_include_ng3: IncludeNinjaGaiden3
    ninja_gaiden_master_collection_ng3_chapter_difficulties: NinjaGaiden3ChapterDifficulties
    ninja_gaiden_master_collection_ng3_mission_difficulties: NinjaGaiden3MissionDifficulties

class NinjaGaidenGame(Game):
    name = "Ninja Gaiden Master Collection"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.PC,
    ]
    is_adult_only_or_unrated = False
    options_cls = NinjaGaidenOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        include_ng2: bool = self.archipelago_options.ninja_gaiden_master_collection_include_ng2.value
        include_ng3: bool = self.archipelago_options.ninja_gaiden_master_collection_include_ng3.value
        if not (include_ng2 or include_ng3):
            raise OptionError("You need to include at least one game")

        templates: List[GameObjectiveTemplate] = []

        if include_ng2:
            ng2_chapter_difficulties: List[str] = self.archipelago_options.ninja_gaiden_master_collection_ng2_chapter_difficulties.value

            templates.append(GameObjectiveTemplate(
                label="NGS2 Chapter select: Complete chapter CHAPTER on DIFFICULTY difficulty",
                data={
                    "CHAPTER": (self.ng2_chapters, 1),
                    "DIFFICULTY": (ng2_chapter_difficulties, 1),
                },
                weight=15
            ))
            templates.append(GameObjectiveTemplate(
                label="NGS2 Chapter select: Complete chapter RYU_CHAPTER on DIFFICULTY difficulty with the WEAPON",
                data={
                    "RYU_CHAPTER": (self.ng2_ryu_chapters, 1),
                    "DIFFICULTY": (ng2_chapter_difficulties, 1),
                    "WEAPON": (self.ng2_weapons, 1),
                },
                weight=20
            ))
            if self.ng2_tag_missions:
                templates.append(GameObjectiveTemplate(
                    label="NGS2 Tag missions: Complete MISSION with CHARACTER1, CHARACTER2",
                    data={
                        "MISSION": (self.ng2_tag_missions, 1),
                        "CHARACTER1": (self.ng2_characters, 1),
                        "CHARACTER2": (self.ng2_characters, 1),
                    },
                    weight=5
                ))
        if include_ng3:
            ng3_chapter_difficulties: List[str] = self.archipelago_options.ninja_gaiden_master_collection_ng3_chapter_difficulties.value
            templates.append(GameObjectiveTemplate(
                label="NG3RE Chapter challenge: Complete CHAPTER on DIFFICULTY difficulty",
                data={
                    "CHAPTER": (self.ng3_chapters, 1),
                    "DIFFICULTY": (ng3_chapter_difficulties, 1),
                },
                weight=15
            ))
            weapons_or_other_characters = [f"the {w}" for w in self.ng3_weapons] + self.ng3_other_characters
            templates.append(GameObjectiveTemplate(
                label="NG3RE Chapter challenge: Complete CHAPTER on DIFFICULTY difficulty with WEAPON_OR_OTHER_CHARACTER",
                data={
                    "CHAPTER": (self.ng3_chapters, 1),
                    "DIFFICULTY": (ng3_chapter_difficulties, 1),
                    "WEAPON_OR_OTHER_CHARACTER": (weapons_or_other_characters, 1),
                },
                weight=20
            ))
            if self.ng3_trials:
                templates.append(GameObjectiveTemplate(
                    label="NG3RE Ninja trials: Complete TRIAL with CHARACTER",
                    data={
                        "TRIAL": (self.ng3_trials, 1),
                        "CHARACTER": (["Hayabusa"] + self.ng3_other_characters, 1),
                    },
                    weight=10
                ))

        return templates

    ng2_chapters = list(str(i) for i in range(1, 18))
    ng2_ryu_chapters = list(str(i) for i in range(1, 18) if i not in [5, 8, 11])
    ng2_weapons = [
        "True Dragon Sword",
        "Vigoorian Flail",
        "Enma's Fang",
        "Tonfa",
        "Eclipse Scythe",
        "Blade of the Archfiend",
        "Kusari-Gama",
        "Falcon's Talons",
        "Lunar Staff",
    ]
    ng2_characters = [
        "Hayabusa",
        "Momiji",
        "Rachel",
        "Ayane",
    ]

    @functools.cached_property
    def ng2_tag_missions(self) -> List[str]:
        difficulties: List[str] = self.archipelago_options.ninja_gaiden_master_collection_ng2_mission_difficulties.value
        mission_number = {
            "Acolyte": 10,
            "Warrior": 10,
            "Mentor": 5,
            "Master Ninja": 5,
            "Ultimate Ninja": 5,
        }

        return [
            f"{d} {i}" for d in difficulties for i in range(1, mission_number[d] + 1)
        ]

    ng3_chapters = [f"Day {d}" for d in range(1, 9)] + [f"Day {d} - Ayane" for d in [2, 6]]
    ng3_weapons = [
        "Dragon Sword",
        "Kusari-Gama",
        "Lunar Staff",
        "Dual Katana",
        "Eclipse Scythe",
        "Falcon's Talons",
    ]
    ng3_other_characters = [
        "Ayane",
        "Momiji",
        "Kasumi",
    ]
    @functools.cached_property
    def ng3_trials(self) -> List[str]:
        difficulties: List[str] = self.archipelago_options.ninja_gaiden_master_collection_ng3_mission_difficulties.value
        mission_number = {
            "Acolyte": 25,
        }

        return [
            f"{d} {i}" for d in difficulties for i in range(1, mission_number[d] + 1)
        ]

class NinjaGaidenChapterDifficulties(OptionSet):
    def verify(self, *args, **kwargs):
        super().verify(*args, **kwargs)
        if not self.value:
            raise OptionError("You need to include at least one game")

class IncludeNinjaGaiden2(DefaultOnToggle):
    """
    Include objectives from Ninja Gaiden Sigma 2.
    """
    display_name = "Include Ninja Gaiden Sigma 2"

class NinjaGaiden2ChapterDifficulties(NinjaGaidenChapterDifficulties):
    """
    Difficulties that may appear in Ninja Gaiden Sigma 2 chapter select objectives.

    Valid values:
    - Acolyte
    - Warrior
    - Mentor
    - Master Ninja
    """
    display_name = "Ninja Gaiden Sigma 2 chapter select difficulties"
    valid_keys = [
        "Acolyte",
        "Warrior",
        "Mentor",
        "Master Ninja",
    ]
    default = ["Warrior"]

class NinjaGaiden2MissionDifficulties(OptionSet):
    """
    Difficulties that may appear in Ninja Gaiden Sigma 2 tag mission objectives.
    An empty list will disable tag mission objectives.

    Valid values:
    - Acolyte
    - Warrior
    - Mentor
    - Master Ninja
    - Ultimate Ninja
    """
    valid_keys = NinjaGaiden2ChapterDifficulties.valid_keys + ["Ultimate Ninja"]
    default = ["Acolyte"]
    display_name = "Ninja Gaiden Sigma 2 tag mission difficulties"

class IncludeNinjaGaiden3(DefaultOnToggle):
    """
    Include objectives from Ninja Gaiden 3: Razor's Edge.
    """
    display_name = "Include Ninja Gaiden 3: Razor's Edge"

class NinjaGaiden3ChapterDifficulties(NinjaGaidenChapterDifficulties):
    """
    Difficulties that may appear in Ninja Gaiden 3 Razor's Edge chapter challenge objectives.

    Valid values:
    - Hero
    - Normal
    - Hard
    - Master Ninja
    - Ultimate Ninja
    """
    display_name = "Ninja Gaiden 3 Razor's Edge chapter challenge difficulties"
    valid_keys = [
        "Hero",
        "Normal",
        "Hard",
        "Master Ninja",
        "Ultimate Ninja",
    ]
    default = ["Normal"]

class NinjaGaiden3MissionDifficulties(OptionSet):
    """
    Difficulties that may appear in Ninja Gaiden 3 Razor's Edge ninja trials objectives.
    An empty list will disable ninja trial objectives.

    Valid values:
    - Acolyte
    """
    valid_keys = [
        "Acolyte"
    ]
    default = ["Acolyte"]
    display_name = "Ninja Gaiden 3 Razor's Edge ninja trial difficulties"
