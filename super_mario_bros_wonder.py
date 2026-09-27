from __future__ import annotations

from typing import List, Optional, TypedDict

from dataclasses import dataclass
import functools

from Options import DefaultOnToggle, OptionError, OptionSet, Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SuperMarioBrosWonderOptions:
    super_mario_bros_wonder_enabled_course_types: SuperMarioBrosWonderEnabledCourseTypes
    super_mario_bros_wonder_max_difficulty: SuperMarioBrosWonderMaxDifficulty
    super_mario_bros_wonder_exclude_courses: SuperMarioBrosWonderExcludeCourses
    super_mario_bros_wonder_include_flagpoles: SuperMarioBrosWonderIncludeFlagpoles
    super_mario_bros_wonder_include_ten_flower_coins: SuperMarioBrosWonderIncludeTenFlowerCoins

class Course(TypedDict):
    world: str
    name: str
    difficulty: int
    type: Optional[str]
    flag: bool
    ten_coins: bool

def course(world: str, name: str, difficulty=0, flag=True, ten_coins=True, type=None) -> Course:
    return {
        "world": world,
        "name": name,
        "difficulty": difficulty,
        "type": type,
        "flag": flag and type not in ["Wiggler Race", "KO Arena", "Break Time!", "Search Party"],
        "ten_coins": ten_coins and type not in ["Wiggler Race", "Break Time!", "Search Party"],
    }

all_courses = [
    course("w1 Pipe-Rock Plateau", "Welcome to the Flower Kingdom!", difficulty=1),
    course("w1 Pipe-Rock Plateau", "Piranha Plant on Parade", difficulty=1),
    course("w1 Pipe-Rock Plateau", "Scram, Skedaddlers!", difficulty=1),
    course("w1 Pipe-Rock Plateau", "Bulrush Coming Through!", difficulty=1),
    course("w1 Pipe-Rock Plateau", "Here Come the Hoppos", difficulty=2),
    course("w1 Pipe-Rock Plateau", "Rolla Koopa Derby", difficulty=2),
    course("w1 Pipe-Rock Plateau", "Swamp Pipe Crawl", difficulty=3),
    course("w1 Pipe-Rock Plateau", "Angry Spikes and Sinkin's Pipes", difficulty=2),
    course("w1 Pipe-Rock Plateau", "Bulrush Express", difficulty=4),
    course("w1 Pipe-Rock Plateau", "Sproings in the Twilight Forest", difficulty=2),
    course("w1 Pipe-Rock Plateau", "Cosmic Hoppos", difficulty=3),
    course("w1 Pipe-Rock Plateau", "Parachute Cap I", type="Badge Challenge", difficulty=1),
    course("w1 Pipe-Rock Plateau", "Wall-Climb Jump I", type="Badge Challenge", difficulty=1),
    course("w1 Pipe-Rock Plateau", "Jet Run I", type="Expert Badge Challenge", difficulty=3),
    course("w1 Pipe-Rock Plateau", "Mountaineering!", type="Wiggler Race", difficulty=1),
    course("w1 Pipe-Rock Plateau", "Pipe-Rock Plateau Palace", flag=False, difficulty=3),
    course("w1 Pipe-Rock Plateau", "Pipe-Rock Rumble", type="KO Arena"),
    course("w1 Pipe-Rock Plateau", "Hurry, Hurry", type="Break Time!"),
    course("w1 Pipe-Rock Plateau", "Wonder Token Tunes", type="Break Time!"),
    course("w1 Pipe-Rock Plateau", "Pop Up, Hoppo!", type="Break Time!"),
    course("w2 Fluff-puff Peaks", "Outmaway Valley", difficulty=3),
    course("w2 Fluff-puff Peaks", "Pokipede Pass", difficulty=1),
    course("w2 Fluff-puff Peaks", "Condarts Away!", difficulty=2),
    course("w2 Fluff-puff Peaks", "Pole Block Passage", difficulty=2),
    course("w2 Fluff-puff Peaks", "Up 'n' Down with Puffy Lifts", difficulty=2),
    course("w2 Fluff-puff Peaks", "Jump! Jump! Jump!", difficulty=4),
    course("w2 Fluff-puff Peaks", "Countdown to Drop Down", difficulty=3),
    course("w2 Fluff-puff Peaks", "Cruising with Linking Lifts", difficulty=2),
    course("w2 Fluff-puff Peaks", "Wall-Climb Jump II", type="Badge Challenge", difficulty=4),
    course("w2 Fluff-puff Peaks", "Floating High Jump I", type="Badge Challenge", difficulty=1),
    course("w2 Fluff-puff Peaks", "Spring Feet I", type="Expert Badge Challenge", difficulty=3),
    course("w2 Fluff-puff Peaks", "Fluff-Puff Peaks Flying Battleship", flag=False, difficulty=3),
    course("w2 Fluff-puff Peaks", "Fluff-Puff Peaks Palace", flag=False, difficulty=4),
    course("w2 Fluff-puff Peaks", "Fluff-Puff Kerfuff", type="KO Arena"),
    course("w2 Fluff-puff Peaks", "Puzzling Park", type="Search Party"),
    course("w2 Fluff-puff Peaks", "Kick it, Outmaway", type="Break Time!"),
    course("w2 Fluff-puff Peaks", "Cloud Cover", type="Break Time!"),
    course("w2 Fluff-puff Peaks", "Zip-Go-Round", type="Break Time!"),
    course("w3 Shining Falls", "The Hoppycat Trial: Hop, Hop, and Awaaay", difficulty=3),
    course("w3 Shining Falls", "The Anglefish Trial: Ready, Aim, Fly!", difficulty=2),
    course("w3 Shining Falls", "The Midway Trial: Hop to It", difficulty=2),
    course("w3 Shining Falls", "The Sharp Trial: Launch to Victory", difficulty=4),
    course("w3 Shining Falls", "The Sugarstar Trial: Across the Night Sky", difficulty=3),
    course("w3 Shining Falls", "The Final Trial: Zip Track Dash", difficulty=3),
    course("w3 Shining Falls", "Crouching High Jump I", type="POOF! Badge Challenge", difficulty=1),
    course("w3 Shining Falls", "An Empty Park?", type="Search Party"),
    course("w3 Shining Falls", "Unreachable Treasure?", type="Break Time!"),
    course("w3 Shining Falls", "Watery Wonder Tokens", type="Break Time!"),
    course("w3 Shining Falls", "Timer-Switch Climb", type="Break Time!"),
    course("w3 Shining Falls", "Timer-Switch Dash", type="Break Time!"),
    course("w4 Sunbaked Desert", "Armads on the Roll", difficulty=3),
    course("w4 Sunbaked Desert", "The Desert Mystery", difficulty=2),
    course("w4 Sunbaked Desert", "Rolling-Ball Hall", difficulty=2),
    course("w4 Sunbaked Desert", "Ninji Jump Party", difficulty=1),
    course("w4 Sunbaked Desert", "Bloomps of the Desert Skies", difficulty=3),
    course("w4 Sunbaked Desert", "Valley Fulla Snootles", difficulty=2),
    course("w4 Sunbaked Desert", "Color-Switch Dungeon", difficulty=2),
    course("w4 Sunbaked Desert", "Secrets of Shova Mansion", difficulty=2),
    course("w4 Sunbaked Desert", "Flight of the Bloomps", difficulty=4),
    course("w4 Sunbaked Desert", "Parachute Cap II", type="Badge Challenge", difficulty=3),
    course("w4 Sunbaked Desert", "Crouching High Jump II", type="Badge Challenge", difficulty=4),
    course("w4 Sunbaked Desert", "Invisibility I", type="Expert Badge Challenge", difficulty=3),
    course("w4 Sunbaked Desert", "Sunbaked Desert Palace", flag=False, difficulty=4),
    course("w4 Sunbaked Desert", "Sunbaked Skirmish", type="KO Arena"),
    course("w4 Sunbaked Desert", "Pipe Park", type="Search Party"),
    course("w4 Sunbaked Desert", "Treasure Vault", type="Break Time!"),
    course("w4 Sunbaked Desert", "Raise the Stage", type="Break Time!"),
    course("w4 Sunbaked Desert", "Revver Run", type="Break Time!"),
    course("w4 Sunbaked Desert", "Floating Wonder Tokens", type="Break Time!"),
    course("w4 Sunbaked Desert", "Bouncy Tunes", type="Break Time!"),
    course("w4 Sunbaked Desert", "Lights Out", type="Break Time!"),
    course("w5 Fungi Mines", "Upshroom Downshroom", difficulty=1),
    course("w5 Fungi Mines", "Taily's Toxic Pond", difficulty=3),
    course("w5 Fungi Mines", "Light-Switch Mansion", difficulty=2),
    course("w5 Fungi Mines", "Beware of the Rifts", difficulty=3),
    course("w5 Fungi Mines", "An Uncharted Area: Wubba Ruins", difficulty=2),
    course("w5 Fungi Mines", "Another Uncharted Area: Swaying Ruins", difficulty=3),
    course("w5 Fungi Mines", "A Final Uncharted Area: Poison Ruins", difficulty=4),
    course("w5 Fungi Mines", "Grappling Vine I", type="Badge Challenge", difficulty=2),
    course("w5 Fungi Mines", "Fungi Funk", type="KO Arena"),
    course("w5 Fungi Mines", "Tumble House", type="Break Time!"),
    course("w5 Fungi Mines", "Trottin's Piranha Plants", type="Break Time!"),
    course("w6 Deep Magma Bog", "Where the Rrrumbas Rule", difficulty=2),
    course("w6 Deep Magma Bog", "Raarghs in the Ruins", difficulty=3),
    course("w6 Deep Magma Bog", "Pull, Turn, Burn", difficulty=4),
    course("w6 Deep Magma Bog", "Hot-Hot Hot!", difficulty=2),
    course("w6 Deep Magma Bog", "Wavy Ride through the Magma Tube", difficulty=4),
    course("w6 Deep Magma Bog", "Dragon Boneyard", difficulty=4),
    course("w6 Deep Magma Bog", "Floating High Jump II", type="Badge Challenge", difficulty=3),
    course("w6 Deep Magma Bog", "Boosting Spin Jump II", type="Badge Challenge", difficulty=3),
    course("w6 Deep Magma Bog", "Grappling Vine II", type="Badge Challenge", difficulty=3),
    course("w6 Deep Magma Bog", "Jet Run II", type="Expert Badge Challenge", difficulty=3),
    course("w6 Deep Magma Bog", "Invisibility II", type="Expert Badge Challenge", difficulty=3),
    course("w6 Deep Magma Bog", "Spring Feet II", type="Expert Badge Challenge", difficulty=4),
    course("w6 Deep Magma Bog", "Deep Magma Bog Flying Battleship", flag=False, difficulty=3),
    course("w6 Deep Magma Bog", "Deep Magma Bog Palace", flag=False, difficulty=4),
    course("w6 Deep Magma Bog", "Magma Flare-Up", type="KO Arena"),
    course("w6 Deep Magma Bog", "Item Park", type="Search Party"),
    course("w6 Deep Magma Bog", "Hot-Hot Rocks", type="Break Time!"),
    course("Petal Isles", "Leaping Smackerel", difficulty=2),
    course("Petal Isles", "Robbird Cove", difficulty=2),
    course("Petal Isles", "Blewbird Roost", difficulty=2),
    course("Petal Isles", "Downpour Uproar", difficulty=3),
    course("Petal Isles", "Jewel-Block Cave", difficulty=2),
    course("Petal Isles", "Gnawsher Lair", difficulty=3),
    course("Petal Isles", "Maw-Maw Mouthful", difficulty=2),
    course("Petal Isles", "Muncher Fields", difficulty=2),
    course("Petal Isles", "Dolphin Kick I", type="Badge Challenge", difficulty=1),
    course("Petal Isles", "Dolphin Kick II", type="Badge Challenge", difficulty=2),
    course("Petal Isles", "Boosting Spin Jump I", type="Badge Challenge", difficulty=1),
    course("Petal Isles", "Swimming!", type="Wiggler Race", difficulty=2),
    course("Petal Isles", "Spelunking!", type="Wiggler Race", difficulty=4),
    course("Petal Isles", "Petal Isles Flying Battleship", flag=False, difficulty=3),
    course("Petal Isles", "Petal Meddle", type="KO Arena"),
    course("Petal Isles", "Missile Meg Mayhem", difficulty=3),
    course("Petal Isles", "High-Voltage Gauntlet", difficulty=4),
    course("Petal Isles", "Evade the Seeker Bullet Bills!", difficulty=4),
    course("Petal Isles", "KnuckleFest Bowser's Blazing Beats", difficulty=4),
    course("Petal Isles", "The Final Battle! Bowser's Rage Stage", flag=False, ten_coins=False, difficulty=5),
    course("Special World", "Pipe-Rock Plateau Special Bounce, Bounce, Bounce", difficulty=5),
    course("Special World", "Fluff-Puff Peaks Special Climb to the Beat", difficulty=5),
    course("Special World", "Shining Falls Special Triple Threat Deluge", difficulty=5),
    course("Special World", "Sunbaked Desert Special Pole Block Allure", difficulty=5),
    course("Special World", "Fungi Mines Special Dangerous Donut Ride", difficulty=5),
    course("Special World", "Deep Magma Bog Special Solar Roller", difficulty=5),
    course("Special World", "Petal Isles Special Way of the Goomba", difficulty=5),
    course("Special World", "The Semifinal Test Piranha Plant Reprise", difficulty=5),
    course("Special World", "The Final Test Wonder Gauntlet", difficulty=5),
    course("Special World", "The Final-Final Test Badge Marathon", difficulty=5),
]

class SuperMarioBrosWonder(Game):
    name = "Super Mario Bros. Wonder"
    platform = KeymastersKeepGamePlatforms.SW
    platforms_other = [
        KeymastersKeepGamePlatforms.SW2,
    ]
    is_adult_only_or_unrated = False
    options_cls = SuperMarioBrosWonderOptions

    def template(self, label: str, courses: List[Course]) -> List[GameObjectiveTemplate]:
        if not courses:
            return []
        else:
            def display_course(c: Course):
                return f"{c["world"]}: {c["name"]}"

            return [GameObjectiveTemplate(
                label=label,
                data={
                    "COURSE": ([display_course(c) for c in courses], 1),
                },
                weight=len(courses),
            )]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            *self.template("Complete COURSE", [c for c in self.courses if c["type"] != "Wiggler Race"]),
            *self.template("Win the race in COURSE", [c for c in self.courses if c["type"] == "Wiggler Race"]),
        ]
        if self.archipelago_options.super_mario_bros_wonder_include_flagpoles.value:
            templates.extend(self.template("Reach the top of the flagpole in COURSE", [c for c in self.courses if c["flag"]]))
        if self.archipelago_options.super_mario_bros_wonder_include_ten_flower_coins.value:
            templates.extend(self.template("Collect all the 10-flower coins in COURSE", [c for c in self.courses if c["ten_coins"]]))

        return templates

    @functools.cached_property
    def courses(self) -> List[Course]:
        def is_enabled(c: Course) -> bool:
            if c["type"] and c["type"] not in self.archipelago_options.super_mario_bros_wonder_enabled_course_types.value:
                return False
            if c["difficulty"] > self.archipelago_options.super_mario_bros_wonder_max_difficulty.value:
                return False
            if c["name"] in self.archipelago_options.super_mario_bros_wonder_exclude_courses.value:
                return False
            return True

        enabled_courses = [c for c in all_courses if is_enabled(c)]
        if not enabled_courses:
            raise OptionError("No enabled course")
        return enabled_courses

class SuperMarioBrosWonderEnabledCourseTypes(OptionSet):
    """
    Course types that may appear in objectives.
    Traditional courses are always enabled.
    """
    valid_keys = frozenset(c["type"] for c in all_courses if c["type"])
    default = valid_keys
    display_name = "Enable course types"

class SuperMarioBrosWonderMaxDifficulty(Range):
    """
    Maximum course difficulty, in stars.
    Courses that don't have a difficulty ratings are not affected by this.
    """
    range_start = 1
    range_end = 5
    default = 5
    display_name = "Maximum course difficulty"

class SuperMarioBrosWonderExcludeCourses(OptionSet):
    """
    Courses that are excluded.
    """
    valid_keys = frozenset(c["name"] for c in all_courses)
    default = []
    display_name = "Excluded courses"

class SuperMarioBrosWonderIncludeFlagpoles(DefaultOnToggle):
    """
    Include objectives that require touching reaching top of the flagpole.
    """
    display_name = "Include flagpoles"

class SuperMarioBrosWonderIncludeTenFlowerCoins(DefaultOnToggle):
    """
    Include objectives that require collecting all of the 10-flower coins in a course.
    """
    display_name = "Include 10-flower coins"
