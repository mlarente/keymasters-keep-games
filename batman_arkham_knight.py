from __future__ import annotations

from typing import List

from dataclasses import dataclass
import functools

from Options import DefaultOnToggle, OptionError, OptionSet, Range, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

challenge_maps = {
    "base": {
        "combat": [
            "Azrael's Atonement",
            "Combo Master",
            "Tower Defense",
        ],
        "combat-dual": [
            "Gotham Knights",
        ],
        "predator": [
            "Revive and Shine",
            "Smash and Grab",
            "Terminal Velocity",
            "Under the Pale Moonlight",
        ],
        "batmobile-race": [
            "Midnight Fury TT",
            "City Heat TT",
            "Crushonator",
            "Condamned",
            "Mental Blocked",
        ],
        "batmobile-combat": [
            "Untouchable",
            "One Man Army",
            "Natural Selection",
            "Slumdog Billionaire",
        ],
        "batmobile-hybrid": [
            "Seek and Destroy",
            "Knight Time Strike",
            "Road Rage",
            "Big Game Hunter",
            "David and Goliath",
            "Drone Zone",
        ],
    },
    "Crime Fighter Challenge Pack 1": {
        "combat": [
            "Cat's Conundrum",
            "Newton's Cradle",
            "Teen Titan",
        ],
        "combat-dual": [
            "Assault on GCPD",
        ],
        "predator": [
            "Deconstruction",
            "Financial Crash",
        ],
    },
    "Crime Fighter Challenge Pack 2": {
        "combat": [
            "Feline Frenzy",
            "Flying Grayson",
            "High Interest",
        ],
        "predator": [
            "Sky High",
        ],
        "predator-dual": [
            "Uncontainable",
        ],
        "batmobile-hybrid": [
            "Armored Assault",
        ],
    },
    "Crime Fighter Challenge Pack 3": {
        "combat": [
            "Precinct",
        ],
        "combat-dual": [
            "Guardians",
        ],
        "predator": [
            "Vertigo",
            "Stage Fright",
        ],
        "predator-dual": [
            "Chemical Reaction",
        ],
        "batmobile-race": [
            "Cauldron Speedway TT",
        ],
    },
    "Crime Fighter Challenge Pack 4": {
        "combat": [
            "Wild Cat",
            "Clockwork",
            "Quarantine",
        ],
        "predator": [
            "Credit Crunch",
            "Divine Intervention",
        ],
        "predator-dual": [
            "High Flyers",
        ],
    },
    "Crime Fighter Challenge Pack 5": {
        "combat": [
            "Hand of God",
            "Flawless",
        ],
        "combat-dual": [
            "Duet",
        ],
        "predator": [
            "Firesale",
            "Psychiatricks",
        ],
        "batmobile-combat": [
            "Graveyard Shift",
        ],
    },
    "Crime Fighter Challenge Pack 6": {
        "combat": [
            "Crime Alley",
            "Monarch Theatre",
            "Iceberg Lounge",
        ],
        "predator": [
            "Wayne Manor",
            "Batcave",
            "Silent Knight",
            "Endless Knight",
        ],
    },
    "Catwoman's Revenge": {
        "combat": [
            "Destruction Line",
        ],
        "predator": [
            "Toy Soldiers",
        ],
    },
    "A Flip of a Coin": {
        "combat": [
            "Scales of Justice",
        ],
        "predator": [
            "Trash Disposal",
        ],
    },
    "GCPD Lockdown": {
        "combat": [
            "Shark Bait",
        ],
        "predator": [
            "Jailbreak",
        ],
    },
    "Scarecrow Nightmares": {
        "scarecrow": [
            "Scarecrow Nightmare 1",
            "Scarecrow Nightmare 2",
            "Scarecrow Nightmare 3",
        ],
    },
}

@dataclass
class ArkhamKnightOptions:
    batman_arkham_knight_included_content: ArkhamKnightIncludedContent

    batman_arkham_knight_include_combat_challenges: ArkhamKnightIncludeCombatChallenges
    batman_arkham_knight_include_predator_challenges: ArkhamKnightIncludePredatorChallenges
    batman_arkham_knight_include_batmobile_race_challenges: ArkhamKnightIncludeBatmobileRaceChallenges
    batman_arkham_knight_include_batmobile_combat_challenges: ArkhamKnightIncludeBatmobileCombatChallenges
    batman_arkham_knight_include_batmobile_hybrid_challenges: ArkhamKnightIncludeBatmobileHybridChallenges
    batman_arkham_knight_include_scarecrow_challenges: ArkhamKnightIncludeScarecrowChallenges

    batman_arkham_knight_max_stars_combat_challenges: ArckamKnightMaxStarsCombatChallenges
    batman_arkham_knight_max_stars_predator_challenges: ArckamKnightMaxStarsPredatorChallenges
    batman_arkham_knight_max_stars_batmobile_race_challenges: ArckamKnightMaxStarsBatmobileRaceChallenges
    batman_arkham_knight_max_stars_batmobile_combat_challenges: ArckamKnightMaxStarsBatmobileCombatChallenges
    batman_arkham_knight_max_stars_batmobile_hybrid_challenges: ArckamKnightMaxStarsBatmobileHybridChallenges
    batman_arkham_knight_max_stars_scarecrow_challenges: ArckamKnightMaxStarsScarecrowChallenges

class ArkhamKnight(Game):
    name = "Batman: Arkham Knight"
    platform = KeymastersKeepGamePlatforms.PS4
    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.SW,
    ]
    is_adult_only_or_unrated = False
    options_cls = ArkhamKnightOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            *self.challenge_template("Combat", "combat", "combat", character_select=True),
            *self.challenge_template("Combat", "combat-dual", "combat", character_select=False),
            *self.challenge_template("Predator", "predator", "predator", character_select=True),
            *self.challenge_template("Predator", "predator-dual", "predator", character_select=False),
            *self.challenge_template("Batmobile race", "batmobile-race", "batmobile_race", character_select=False),
            *self.challenge_template("Batmobile combat", "batmobile-combat", "batmobile_combat", character_select=False),
            *self.challenge_template("Batmobile hybrid", "batmobile-hybrid", "batmobile_hybrid", character_select=False),
            *self.challenge_template("Scarecrow", "scarecrow", "scarecrow", character_select=False),
        ]

        if not templates:
            raise OptionError("You must enable at least one type of challenge")

        return templates

    def challenge_template(self, challenge_label: str, map_type: str, challenge_option: str, character_select=False) -> List[GameObjectiveTemplate]:
        if not self.get_option("include", challenge_option):
            return []
        star_ratings = ["one star", "two stars", "three stars"][:self.get_option("max_stars", challenge_option)]

        maps: List[str] = []
        for dlc_name, dlc_content in challenge_maps.items():
            if dlc_name == "base" or dlc_name in self.included_content:
                maps.extend(dlc_content.get(map_type, []))
        if not maps:
            return []

        data={
            "CHALLENGE_MAP": (maps, 1),
            "STAR_RATING": (star_ratings, 1),
        }
        if character_select:
            label = f"{challenge_label} challenge: complete CHALLENGE_MAP with STAR_RATING as CHARACTER"
            data["CHARACTER"] = (self.characters, 1)
        else:
            label = f"{challenge_label} challenge: complete CHALLENGE_MAP with STAR_RATING"

        return [GameObjectiveTemplate(label=label, data=data, weight=len(maps))]

    def get_option(self, option_name: str, challenge_option: str):
        return getattr(self.archipelago_options, f"batman_arkham_knight_{option_name}_{challenge_option}_challenges").value

    @functools.cached_property
    def included_content(self) -> List[str]:
        return self.archipelago_options.batman_arkham_knight_included_content.value

    @functools.cached_property
    def characters(self) -> List[str]:
        c = ["Batman", "Azrael"]
        if "A Flip of a Coin" in self.included_content:
            c.append("Robin")
        if "GCPD Lockdown" in self.included_content:
            c.append("Nightwing")
        if "Catwoman's Revenge" in self.included_content:
            c.append("Catwoman")
        if "Red Hood Story Pack" in self.included_content:
            c.append("Red Hood")
        if "A Matter of Family" in self.included_content:
            c.append("Batgirl")
        if "Harley Quinn Story Pack" in self.included_content:
            c.append("Harley Quinn")
        return c

class ArkhamKnightIncludedContent(OptionSet):
    """
    Content from which to pick challenge maps for objectives.
    """
    display_name = "Included content"
    valid_keys = [k for k in challenge_maps.keys() if k != "base"] + [
        "Harley Quinn Story Pack",
        "A Matter of Family",
        "Red Hood Story Pack",
    ]
    default = valid_keys[:]

class ArkhamKnightIncludeCombatChallenges(DefaultOnToggle):
    """
    Include combat challenges.
    """
    display_name = "Include combat challenges"

class ArkhamKnightIncludePredatorChallenges(DefaultOnToggle):
    """
    Include predator challenges.
    """
    display_name = "Include predator challenges"

class ArkhamKnightIncludeBatmobileRaceChallenges(Toggle):
    """
    Include batmobile race challenges.
    """
    display_name = "Include batmobile race challenges"

class ArkhamKnightIncludeBatmobileCombatChallenges(Toggle):
    """
    Include batmobile combat challenges.
    """
    display_name = "Include batmobile combat challenges"

class ArkhamKnightIncludeBatmobileHybridChallenges(Toggle):
    """
    Include batmobile hybrid challenges.
    """
    display_name = "Include batmobile hybrid challenges"

class ArkhamKnightIncludeScarecrowChallenges(Toggle):
    """
    Include scarecrow challenges.
    """
    display_name = "Include scarecrow challenges"

class StarRange(Range):
    range_start = 1
    range_end = 3
    default = 2

class ArckamKnightMaxStarsCombatChallenges(StarRange):
    """
    Maximum star rating that an objective may ask for in combat challenges.
    """
    display_name = "Maximum stars in combat challenges"

class ArckamKnightMaxStarsPredatorChallenges(StarRange):
    """
    Maximum star rating that an objective may ask for in predator challenges.
    """
    display_name = "Maximum stars in predator challenges"

class ArckamKnightMaxStarsBatmobileRaceChallenges(StarRange):
    """
    Maximum star rating that an objective may ask for in batmobile race challenges.
    """
    display_name = "Maximum stars in batmobile race challenges"

class ArckamKnightMaxStarsBatmobileCombatChallenges(StarRange):
    """
    Maximum star rating that an objective may ask for in batmobile combat challenges.
    """
    display_name = "Maximum stars in batmobile combat challenges"

class ArckamKnightMaxStarsBatmobileHybridChallenges(StarRange):
    """
    Maximum star rating that an objective may ask for in batmobile hybrid challenges.
    """
    display_name = "Maximum stars in batmobile hybrid challenges"

class ArckamKnightMaxStarsScarecrowChallenges(StarRange):
    """
    Maximum star rating that an objective may ask for in scarecrow challenges.
    """
    display_name = "Maximum stars in scarecrow challenges"
