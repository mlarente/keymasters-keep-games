from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ShovelKnightOptions:
    shovel_knight_enabled_content: ShovelKnightEnabledContent
    shovel_knight_enable_joustus: ShovelKnightEnableJoustus

class ShoveLKnight(Game):
    name = "Shovel Knight"
    platform = KeymastersKeepGamePlatforms.PC
    platforms_other = [
        KeymastersKeepGamePlatforms._3DS,
        KeymastersKeepGamePlatforms.WIIU,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.VITA,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.FIRE,
        KeymastersKeepGamePlatforms.SW,
    ]
    is_adult_only_or_unrated = False
    options_cls = ShovelKnightOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        enabled_content = self.archipelago_options.shovel_knight_enabled_content.value

        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label='Shovel of Hope: complete the level "LEVEL"',
                data={
                    "LEVEL": (self.shovel_of_hope_levels, 1),
                },
                weight=10,
            ),
        ]

        if "Plague of Shadows" in enabled_content:
            templates.append(GameObjectiveTemplate(
                label='Plague of Shadows: complete the level "LEVEL"',
                data={
                    "LEVEL": (self.plague_of_shadows_levels, 1),
                },
                weight=10
            ))

        if "Specter of Torment" in enabled_content:
            templates.append(GameObjectiveTemplate(
                label='Specter of Torment: complete the level "LEVEL"',
                data={
                    "LEVEL": (self.specter_of_torment_levels, 1),
                },
                weight=10
            ))

        if "King of Cards" in enabled_content:
            templates.append(GameObjectiveTemplate(
                label='King of Cards: complete the level "LEVEL"',
                data={
                    "LEVEL": (self.king_of_cards_levels, 1),
                },
                weight=10
            ))
            if self.archipelago_options.shovel_knight_enable_joustus.value:
                templates.append(GameObjectiveTemplate(
                    label='King of Cards: win a game of joustus against OPPONENT',
                    data={
                        "OPPONENT": (self.joustus_opponents, 1),
                    },
                    weight=10
                ))

        if "Showdown" in enabled_content:
            templates.append(GameObjectiveTemplate(
                label='Showdown: complete story mode as CHARACTER',
                data={
                    "CHARACTER": (self.showdown_characters, 1),
                },
                weight=10
            ))
            templates.append(GameObjectiveTemplate(
                label='Showdown: win a MODE battle as CHARACTER against OPPONENTS',
                data={
                    "MODE": (self.showdown_modes, 1),
                    "CHARACTER": (self.showdown_characters, 1),
                    "OPPONENTS": (self.showdown_characters, [1, 2, 3]),
                },
                weight=6
            ))
            templates.append(GameObjectiveTemplate(
                label='Showdown: win a MODE battle as CHARACTER against OPPONENTS with CHEATS',
                data={
                    "MODE": (self.showdown_modes, 1),
                    "CHARACTER": (self.showdown_characters, 1),
                    "OPPONENTS": (self.showdown_characters, [1, 2, 3]),
                    "CHEATS": (self.showdown_cheats, [1, 2, 3]),
                },
                weight=4
            ))

        return templates

    shovel_of_hope_levels = [
        "Plains",
        "Pridemoor Keep",
        "The Lich Yard",
        "Explodatorium",
        "Iron Whale",
        "Lost City",
        "Stranded Ship",
        "Clockwork Tower",
        "Flying Machine",
        "Tower of Fate: Entrance",
        "Tower of Fate: Ascent",
        "Tower of Fate: ????",
    ]
    plague_of_shadows_levels = shovel_of_hope_levels
    specter_of_torment_levels = [lvl for lvl in shovel_of_hope_levels if lvl != "Tower of Fate: Ascent"]
    king_of_cards_levels = [
        "Plains - Valley of Dawn (world 1)",
        "Plains - Mossy Mountain (world 1)",
        "Plains - Spectral Ravine (world 1)",
        "The Lich Yard - Sunken Town (world 1)",
        "The Lich Yard - Ectoplasm Chasm (world 1)",
        "Pridemorr Keep - Bounding Battlements (world 1)",
        "Pridemorr Keep - Enchanted Conclave (world 1)",
        "Pridemorr Keep - Grand Hall (world 1)",
        "Troupple Pond - Floating Frog Fen (world 2)",
        "Troupple Pond - Axolongl Alcove (world 2)",
        "Troupple Pond - Royal Pond (world 2)",
        "Lost City - Excavation Station (world 2)",
        "Lost City - Bohto's Big Bounce (world 2)",
        "Lost City - Goo Gorge (world 2)",
        "Iron Whale - Lunkeroth's Lagoon (world 2)",
        "Iron Whale - Deep Sea Trench (world 2)",
        "Explodatorium - Pressure Plant (world 2)",
        "Explodatorium - Alchemical Aqueducts (world 2)",
        "Explodatorium - Ratsploder Runway (world 2)",
        "Stranded Ship - Slippery Summit (world 3)",
        "Stranded Ship - Spinwulf Sanctuary (world 3)",
        "Birder Bluffs - Cyclone Sierra (world 3)",
        "Birder Bluffs - King's Roost (world 3)",
        "Clockwork Tower - Shock Assembly (world 3)",
        "Clockwork Tower - Torque Lift Torsion (world 3)",
        "Flying Machine - Aerial Brigade (world 3)",
        "Flying Machine - Ladder Factory (world 3)",
        "Flying Machine - Heavyweight Heights (world 3)",
        "Tower of Fate - Shrouded Spires (world 4)",
        "Tower of Fate - Lava Well (world 4)",
        "Tower of Fate - Warp Wrap Keep (world 4)",
        "Tower of Fate - ???? (world 4)",
    ]
    joustus_opponents = [
        "Baz (Airship)",
        "Hedge Pupil (Airship)",
        "Duelist Di (Airship)",
        "Traitorous (Airship)",
        "Phantom Striker (Airship)",
        "Troupple Acolyte (Airship)",
        "Plague Knight (Airship)",
        "Skip (Airship)",
        "Barton (Airship)",
        "Treasure Knight (Airship)",
        "Mole Knight (Airship)",
        "TMK-500 (Airship)",
        "Propeller Knight (Airship)",
        "Tinker Knight (Airship)",
        "Polar Knight (Airship)",
        "Specter Knight (Airship)",
        "Rookie (House of Joustus - world 1)",
        "Playing Kid (House of Joustus - world 1)",
        "Goatician (House of Joustus - world 1)",
        "Ruffian (House of Joustus - world 1)",
        "Black Knight (House of Joustus - world 1)",
        "Armorer & Shovel Smith (Cavern of Joustus - world 2)",
        "Blazorb (Cavern of Joustus - world 2)",
        "Blorb (Cavern of Joustus - world 2)",
        "Mole Minion (Cavern of Joustus - world 2)",
        "Mona (Cavern of Joustus - world 2)",
        "Leo (Crag of Joustus - world 3)",
        "Cogslotter (Crag of Joustus - world 3)",
        "Hover Meanie (Crag of Joustus - world 3)",
        "Spinwulves (Crag of Joustus - world 3)",
        "Missy (Tower of Joustus - world 4)",
        "Red (Tower of Joustus - world 4)",
        "Liquid Samurai (Tower of Joustus - world 4)",
        "Horace (Tower of Joustus - world 4)",
    ]
    showdown_characters = [
        "Shovel Knight",
        "Plague Knight",
        "Specter Knight",
        "King Knight",
        "Shield Knight",
        "Black Knight",
        "Propeller Knight",
        "Mole Knight",
        "Polar Knight",
        "Tinker Knight",
        "The Enchantress",
        "Baz",
        "Phantom Striker",
        "Mona",
    ]
    showdown_modes = ["Treasure Clash", "Showdown"]
    showdown_cheats = [
        "High jump",
        "Fast run",
        "Giant characters",
        "Strong knockback",
        "4x damage",
        "Ignore player damage",
        "2 health max",
        "KO drops all gems",
        "Slow motion",
        "Fast motion",
        "Beeto breach",
        "Forever fairies",
        "Hurricane",
    ]

class ShovelKnightEnabledContent(OptionSet):
    """
    Enabled content that may appear in objectives.
    Objectives from the main compaign are always enabled.

    Valid values:
    - Plague of Shadows
    - Specter of Torment
    - King of Cards
    - Showdown
    """
    display_name = "Enabled content"
    valid_keys = [
        "Plague of Shadows",
        "Specter of Torment",
        "King of Cards",
        "Showdown",
    ]
    default = valid_keys[:]

class ShovelKnightEnableJoustus(DefaultOnToggle):
    """
    Enable the Joustus card game.
    Only relevant when King of Cards content is enabled.
    """
    display_name = "Enable Joustus"
