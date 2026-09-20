from __future__ import annotations

from typing import Any, List, NotRequired, TypedDict

from dataclasses import dataclass

from Options import Option, OptionError

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MediaLibraryOptions:
    media_libraries: MediaLibrariesOption

class MediaLibrary(Game):
    name = "Media Library"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = MediaLibraryOptions

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        libraries: List[MediaLibraryOption] = self.archipelago_options.media_libraries.value
        fullLibraries: List[MediaLibraryOption] = (
            {
                "weight": int(library.get("weight", 1)),
                "action": library.get("action", None) or "Enjoy",
                "library": library["library"],
            }
            for library in libraries
        )
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label=f"{library["action"]} MEDIA",
                data={"MEDIA": (library["library"], 1)},
                weight=library["weight"],
            )
            for library in fullLibraries
            if library["weight"]
        ]
        if not templates:
            raise OptionError("No active media library")
        return templates

class MediaLibraryOption(TypedDict):
    weight: NotRequired[int]
    action: NotRequired[str]
    library: List[str]

class MediaLibrariesOption(Option[List[MediaLibraryOption]]):
    """
    Media libraries to select media from.
    It should look like this:

    media_libraries:
      - weight: 10
        action: Watch
        library:
          - "Frieren: Beyond Journey's End"
          - Steins;Gate
      - weight: 20
        action: Read
        library:
          - 20th Century Boys
          - Monster

    The above example creates objectives like "Watch Steins;Gate" or "Read Monster" with twice as much chance to select
    a book.
    If omitted, `weight` defaults to 1. `action` defaults to "Enjoy".
    """

    display_name = "Media libraries"
    supports_weighting = False
    default: List[MediaLibraryOption] = [{
        "weight": 50,
        "action": "Watch",
        "library": ["A movie", "A TV series"],
    }]

    def __init__(self, value: List[MediaLibraryOption]):
        self.value = value

    @classmethod
    def from_any(cls, data: dict[str, Any]) -> MediaLibrariesOption:
        if isinstance(data, list):
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-list, got {type(data)}")

    @classmethod
    def get_option_name(cls, value):
        return ", ".join(map(str, value))

    def verify(self, *args, **kwargs):
        if not isinstance(self.value, list):
            raise OptionError("Invalid media_libraries")
        for library in self.value:
            if not isinstance(library, dict):
                raise OptionError("Invalid media library: " + repr(library))

            try:
                if int(library.get("weight", 1)) < 0:
                    raise ValueError()
            except ValueError:
                raise OptionError("Invalid media library weight: " + repr(library["weight"]))

            if not isinstance(library.get("action", ""), str):
                raise OptionError("Invalid media library action: " + repr(library["action"]))

            if not isinstance(library.get("library", None), list):
                raise OptionError("Invalid or missing media library: " + repr(library))
            for media in library:
                if not isinstance(media, str):
                    raise OptionError("Invalid media library entry: " + repr(media))
