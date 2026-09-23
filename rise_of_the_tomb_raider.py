from __future__ import annotations

from typing import Dict, List, TypedDict

from dataclasses import dataclass
import functools

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


class ChapterChallenges(TypedDict):
    base: List[str]
    timed: List[str]

@dataclass
class RiseOfTheTombRaiderOptions:
    rise_of_the_tomb_raider_include_deathless_survivor: IncludeDeathlessSurvivor
    rise_of_the_tomb_raider_include_timed_chapter_challenges: IncludeTimeChapterChallenges

class RiseOfTheTombRaiderGame(Game):
    name = "Rise of the Tomb Raider"
    platform = KeymastersKeepGamePlatforms.X360
    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW2,
    ]
    is_adult_only_or_unrated = False
    options_cls = RiseOfTheTombRaiderOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Endurance: Survive DAYS days and escapeCONDITION",
                data={
                    "DAYS": (list(range(2, 11)), 1),
                    "CONDITION": (self.endurance_extra_conditions, 1),
                },
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Endurance: Gather ARTIFACTS artifacts and escapeCONDITION",
                data={
                    "ARTIFACTS": (list(range(5, 16)), 1),
                    "CONDITION": (self.endurance_extra_conditions, 1),
                },
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Endurance: Complete these challenges: CHALLENGES",
                data={
                    "CHALLENGES": (self.endurance_challenges, self.challenge_qty),
                },
                weight=2,
            ),
            GameObjectiveTemplate(
                label='Chapter replay: Complete "CHAPTER"CONDITION',
                data={
                    "CHAPTER": (self.chapter_replay_chapters, 1),
                    "CONDITION": (self.chapter_replay_extra_conditions, 1),
                },
                weight=2,
            ),
            GameObjectiveTemplate(
                label='Chapter replay elite: Complete "CHAPTER"CONDITION',
                data={
                    "CHAPTER": (self.chapter_replay_elite_chapters, 1),
                    "CONDITION": (self.chapter_replay_elite_extra_conditions, 1),
                },
                weight=2,
            ),
            GameObjectiveTemplate(
                label='Chapter replay: CHAPTER_CHALLENGE',
                data={
                    "CHAPTER_CHALLENGE": (self.all_chapter_replay_challenges(is_elite=False), 1),
                },
                weight=2,
            ),
            GameObjectiveTemplate(
                label='Chapter replay elite: CHAPTER_CHALLENGE',
                data={
                    "CHAPTER_CHALLENGE": (self.all_chapter_replay_challenges(is_elite=True), 1),
                },
                weight=2,
            ),
        ]

        return templates

    endurance_challenges = [
        "Who needs a map?", # Locate 5 crypts
        "Archaeologist", # Collect at least 5 Artifacts in a single expedition
        "Master archaeologist", # Collect at least 10 Artifacts in a single expedition
        "The old ways", # Collect all the parts for Grim Whisper Bow
        "Raider", # Open 5 Codices or Sarcofagi
        "Skillful raider", # Open 5 Codices or Sarcophagi without getting caught in a trap
        "Fast reflexes", # Destroy 3 ceiling traps after being caught in them
        "Observant", # Activate 3 ankle traps without being caught in them
        "Well done", # Eat the meat of 5 birds, squirrels or rabbits killed with fire
        "Overcooked", # Eat the meat of 5 deer killed with explosive arrows
        "Still tastes good", # Eat the meat of 5 wolves that were killed with poison damage
        "Carnivore", # Eat 1 of every animal
        "Happy camper", # Survive for 5 days
        "Nature retreat", # Survive for 7 days
        "Great outdoors", # Survive for 10 days
        "Survivalist", # Survive 5 days without ever freezing or starving
        "Nope", # Escape the forest on day 1 without recovering any artifacts
        "Vegetarian", # Escape after surviving for 3 days, with at least 3 artifacts, without eating meat
        "Vacation", # Escape the forest after surviving for 7 days
        "Great haul", # Escape the forest after surviving for 10 days, with at least 10 Artifacts
        "Roughed up", # Escape the forest while both freezing and starving
        "Great escape", # Escape the Siberian wilderness with 5 or more Artifacts
        "Great escape II", # Escape the Siberian wilderness with 10 or more Artifacts
        "A little late", # Open the chest in the back of the snowcat after collecting 5 artifacts
        "One way to do it", # Warm up from freezinf by standing in fire
        "Nomad", # Light 5 base camps
        "Ice in the veins", # Kill 5 enemies while freezing
        "Sharpshooter", # Kill 10 birds
        "Deer hunter", # Kill 10 deer
        "Hare-brained", # Kill 10 rabbits
        "Small game", # Kill 5 squirrels
        "Packmaster", # Kill 7 wolves
        "Call me curiosity", # Kill 5 giant cats
        "Overbearing", # Kill 5 bears
        "Desperate measurea", # Kill a bear while starving
        "Archer", # Kill 5 enemies with the bow
        "Quiet killer", # Stealth kill 5 enemies with the bow
        "Into darkness", # Kill 5 enemies with melee finishers
        "Accurate", # Kill 5 enemies with melee headshots
        "Bullet holes", # Execute 10 enemies with head shots using a pistol
        "Shadow killer", # Kill 15 enemies undetected
        "Brawler", # Kill 5 enemies with melee attacks
        "Backstabber", # Kill 5 enemies with a melee stealth attack
        "Cocktail party", # Kill 5 enemies using molotovs
        "Gunslinger", # Kill 3 enemies with the pistol
        "Poisonous", # Kill 5 enemies with poison arrows
        "Riddled with holes", # Kill 5 enemies with the rifle
        "Close quarters", # Kill 5 enemies with the shotgun
    ]

    chapter_replay_challenges: Dict[str, ChapterChallenges] = {
        "Mountain peak": {
            "base": [
                "Deathless",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Prophet's Tomb": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Executioner",
                "Lucky penny",
                "Puzzle master II",
                "Puzzle master III",
                "Collector",
            ],
            "timed": [
                "Marksman",
                "Puzzle master",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Siberian Wilderness": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Quiet killer",
                "Backstabber",
                "Brawler",
                "Lobotomy",
                "Into darkness",
                "Looking up",
                "Stealth streak",
                "Kill streak",
                "Shadow warrior",
                "Bear necessities",
                "Poison-less",
                "Bear knuckled",
                "Collector",
                "In the shadows",
            ],
            "timed": [
                "Kneecapped",
                "Eagle eyed",
                "Moving target",
                "A swift death",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Lost Expedition": {
            "base": [
                "Deathless",
                "Cranked",
                "Collector",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Soviet Installation": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Marksman", # speed
                "Shadow warrior",
                "Into darkness",
                "Brawler",
                "Kill streak",
                "Stealth streak",
                "Lobotomy",
                "Bullet holes",
                "Bookworm",
                "Firebug",
                "Shadow II",
                "Shadow",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Hunting Grounds": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Hare-brained",
                "Small game",
                "Packmaster",
                "Deer hunter",
                "Sharpshooter",
                "Lobotomy",
                "Bullet holes",
                "Into darkness",
                "Brawler",
            ],
            "timed": [
                "All bite",
                "Kneecapped",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Ancient Cistern": {
            "base": [
                "Collector",
                "Perfectionist",
                "Waste not",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Soviet Gulag": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Collector",
                "Data corruption",
                "Resourceful",
                "Courtyard hunter",
                "Accurate",
                "Wings of death",
                "Shadow warrior",
                "Into darkness",
                "Brawler",
                "Archer",
                "Gunslinger",
                "Riddled with holes",
                "Lobotomy",
                "Ka-boom",
                "Kill streak",
                "Stealth streak",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Voice of God": {
            "base": [
                "Deathless",
                "Archeology",
                "Collector",
                "Perfect timing",
                "Ornitologist",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Wicked Vale": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Brawler",
                "Archer",
                "Gunslinger",
                "Riddled with holes",
            ],
            "timed": [
                "Marksman",
            ]
        },
        "Return to the Wicked Vale": {
            "base": [],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Whitch's Cave": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Accurate",
                "Into darkness",
                "Brawler",
                "Archer",
                "Gunslinger",
                "Riddled with holes",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Copper Mill": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Into darkness",
                "Brawler",
                "Archer",
                "Cocktail party",
                "Gunsligner",
                "Riddled with holes",
                "Out of the frying pan",
                "Stealthy",
                "Unscathed",
                "Without a trace",
                "Bookworm",
                "History buff",
            ],
            "timed": [
                "Marksman",
                "Short work",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Red Mine": {
            "base": [
                "Deathless",
                "Collector",
                "Geologist",
                "Puzzle master",
                "Puzzle master II",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Prophet's Blessing": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Into darkness",
                "Brawler",
                "Archer",
                "Gunslinger",
                "Riddled with holes",
                "Resourceful",
                "Kill streak",
                "Stealth streak",
                "Defaced",
                "Collector",
                "Shivved",
                "Dropping in",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "House of the Afflicted": {
            "base": [
                "Sharpshooter",
                "Collector",
                "Ornithologist",
                "Water conservationist",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Village": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Into darkness",
                "Brawler",
                "Kill streak",
                "Lobotomy",
                "Bullet holes",
                "Thunderball",
                "Fireproof",
                "Bookworm"
            ],
            "timed": [
                "Rampage",
                "Eagle eyed",
                "Firefighter",
                "Swift ascent",
                "Sense of urgency",
                "Nock nock",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Catacomb of Sacred Waters": {
            "base": [
                "Deathless",
                "Collector",
                "Stay dry",
            ],
            "timed": [
                "Speed boat",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Acropolis": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Lobotomy",
                "Into darkness",
                "Brawler",
                "Quiet killer",
                "Gunslinger",
                "Thunderball",
                "Riddled with holes",
                "Poisonous",
                "Kill streak",
                "Stealth streak",
                "Collector",
                "Crafty",
                "Giving thanks",
                "Courtyard ghost",
                "Courtyard hunter",
            ],
            "timed": [
                "Kneecapped",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Tower": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Lobotomy",
                "Into darkness",
                "Brawler",
                "Gunslinger",
                "Thunderball",
                "Riddled with holes",
                "Poisonous",
                "Bottle rocket",
                "Kill streak",
                "Collector",
                "Burning bridges",
                "I know what these do",
                "Left hanging",
                "Communication breakdown",
            ],
            "timed": [
                "Kneecapped",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Pit of Judgment": {
            "base": [
                "Deathless",
                "Collector",
            ],
            "timed": [
                "Efficient timing",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Approaching Storm": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "In the shadows",
                "Shadow warrior",
                "Bottle rocket",
                "Poisonous",
                "Shadow killer",
                "Accurate",
                "Into darkness",
                "Brawler",
                "Lobotomy",
                "Bullet holes",
                "Stealth streak",
                "Kill streak",
                "Resourceful",
                "Bookworm",
                "Back to basics",
                "Master of the hunt",
            ],
            "timed": [
                "Rampage",
                "Cat-like reflexes",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Flooded Archives": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Into darkness",
                "Brawler",
                "Archer",
                "Gunslinger",
                "Riddled with holes",
                "Resourceful",
                "Kill streak",
                "Cocktail party",
                "From the deep",
                "Cocktail mixer",
                "Up in smoke",
                "Collector",
            ],
            "timed": [
                "Rampage",
                "Demolitions expert",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Baths of Kitezh": {
            "base": [
                "Perfect puzzle",
                "Sweet moves",
            ],
            "timed": [
                "Hydrophobic",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Research Base": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Looking up",
                "Shadow warrior",
                "From the deep",
                "Into darkness",
                "Brawler",
                "Archer",
                "Gunslinger",
                "Riddled with holes",
                "Close quarters",
                "Kill streak",
                "Stealth streak",
                "Collector",
                "Scorched earth",
                "Ghost in the smoke",
                "Silent forest",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Orrery": {
            "base": [
                "Deathless",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Path of the Deathless": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Into darkness",
                "Brawler",
                "Archer",
                "Bottle rocket",
                "Gunslinger",
                "Close quarters",
                "Riddled with holes",
                "Resourceful",
                "Kill streak",
            ],
            "timed": [
                "Kneecapped",
                "Rampage",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Gate of Kitezh": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
                "Accurate",
                "Into darkness",
                "Archer",
                "Gunslinger",
                "Close quarters",
                "Riddled with holes",
                "Resourceful",
                "Bottle rocket",
                "Poisonous",
                "Kill streak",
                "Burn baby burn",
                "First try!",
                "Wheeee!",
                "For whom the bell tolls",
                "Banner wars",
                "Master of combat",
                "Bookworm",
                "History buff",
            ],
            "timed": [
                "Hurried",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Chamber of Exorcism": {
            "base": [
                "Untouchable",
                "Collector",
                "Waste not",
                "Efficient",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Outskirts of Kitezh": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Accurate",
                "Into darkness",
                "Archer",
                "Gunslinger",
                "Close quarters",
                "Riddled with holes",
                "Resourceful",
                "Bottle rocket",
                "Kill streak",
                "Squish",
                "Burn baby burn",
                "Vandal",
            ],
            "timed": [
                "Puzzle master",
                "Puzzle master II",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "The Lost City": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Untouchable",
            ],
            "timed": [
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
        "Chamber of Souls": {
            "base": [
                "Deathless",
                "Deathless survivor",
                "Accurate",
                "Into darkness",
                "Archer",
                "Gunslinger",
                "Riddled with holes",
                "Resourceful",
                "Poisonous",
                "Bottle rocket",
                "An axe to grind",
                "Perfect aim",
                "Bring down the fire",
            ],
            "timed": [
                "Rampage",
                "Speed runner",
                "Speed runner II",
                "Speed runner III",
            ]
        },
    }

    @functools.cached_property
    def chapter_replay_chapters(self):
        return list(self.chapter_replay_challenges.keys())

    @functools.cached_property
    def chapter_replay_elite_chapters(self):
        return list(self.chapter_replay_challenges.keys())[1:]

    challenge_qty = list(range(2, 6))

    bonus_conditions = [
        f" with a minimum card bonus of {n}%" for n in [
            "-30",
            "0",
            "+30",
            "+60",
        ]
    ]
    skill_conditions = [" starting with no skills"] + [
        f" starting with only {s} skills" for s in [
            "adventurer level",
            "professional level",
            "brawler",
            "hunter",
            "survivor",
        ]
    ]

    @functools.cached_property
    def endurance_extra_conditions(self) -> List[str]:
        no_condition = [""] * ((len(self.bonus_conditions) + len(self.skill_conditions)) // 2)
        return [
            *no_condition,
            *self.bonus_conditions,
            *self.skill_conditions,
        ]

    @functools.cached_property
    def chapter_replay_extra_conditions(self) -> List[str]:
        no_condition = [""] * ((len(self.bonus_conditions) + len(self.skill_conditions)) // 2)
        return [
            *no_condition,
            *self.bonus_conditions,
            *self.skill_conditions,
        ]

    @functools.cached_property
    def chapter_replay_elite_extra_conditions(self) -> List[str]:
        no_condition = [""] * ((len(self.bonus_conditions) + len(self.skill_conditions)) // 2)
        return [
            *no_condition,
            *self.bonus_conditions,
        ]

    def all_chapter_replay_challenges(self, is_elite: bool) -> List[str]:
        include_deathless_survivor = self.archipelago_options.rise_of_the_tomb_raider_include_deathless_survivor.value
        include_timed = self.archipelago_options.rise_of_the_tomb_raider_include_timed_chapter_challenges.value

        challenges: List[str] = []

        for chapter in list(self.chapter_replay_challenges.keys())[1 if is_elite else 0:]:
            challenges.extend(
                self.to_chapter_challenge_string(chapter, challenge)
                for challenge in self.chapter_replay_challenges[chapter]["base"]
                if challenge != "Deathless survivor" or include_deathless_survivor
            )
            if include_timed:
                challenges.extend(
                    self.to_chapter_challenge_string(chapter, challenge)
                    for challenge in self.chapter_replay_challenges[chapter]["timed"]
                )

        return challenges

    def to_chapter_challenge_string(self, chapter: str, challenge: str):
        return f'in "{chapter}", complete the "{challenge}" challenge'

class IncludeDeathlessSurvivor(Toggle):
    """
    Include "Deathless survivor" challenges.
    Only available if you're playing on Survivor difficulty.
    """
    display_name = 'Include "Deathless survivor" challenges'

class IncludeTimeChapterChallenges(Toggle):
    """
    Include timed chapter challenges.
    """
    display_name = "Include timed chapter challenges"
