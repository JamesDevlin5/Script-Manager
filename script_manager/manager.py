#!/usr/bin/env python3

from pathlib import Path
import typing


class Color:
    # Map of the color's names to their respective index (internally)
    # Lowercase all color names to avoid case-sensitive matching
    ColorMap = [
        name.lower()
        for name in [
            "Black",
            "Red",
            "Green",
            "Yellow",
            "Blue",
            "Purple",
            "Teal",
            "White",
        ]
    ]
    # And the code to reset all these style changes
    Reset = 0

    @staticmethod
    def _encode_num(color_code: int) -> str:
        # <Esc>[<Num>m ...string message... <Esc>[0m
        return "\x1B[" + str(color_code) + "m"

    @classmethod
    def _map_lookup(cls, name: str, code_map: list[int]) -> str:
        """Utility function to print a color, additionally given a map to translate the colors into codes"""
        # Gets the integer-index that is internally associated with the color name argument
        color_idx = cls.ColorMap.index(name.lower())
        color_code = code_map[:][color_idx]
        return cls._encode_num(color_code)

    @classmethod
    def fg(cls, name: str) -> int:
        """ANSI foreground color code"""
        return cls._map_lookup(name, [30, 31, 32, 33, 34, 35, 36, 37])

    @classmethod
    def bg(cls, name: str) -> int:
        """ANSI background color code"""
        return cls._map_lookup(name, [40, 41, 42, 43, 44, 45, 46, 47])

    @classmethod
    def reset(cls) -> str:
        """Gets the code sequence to reset all attribute stylings"""
        return cls._encode_num(cls.Reset)


class BrightColor(Color):
    """ANSI bright/bold/... form of an escaped color code"""

    @classmethod
    def fg(cls, name: str) -> int:
        """ANSI bright foreground color code"""
        return cls._map_lookup(name, [90, 91, 92, 93, 94, 95, 96, 97])

    @classmethod
    def bg(cls, name: str) -> int:
        """ANSI bright background color code"""
        return cls._map_lookup(name, [100, 101, 102, 103, 104, 105, 106, 107])


class ScriptFile:
    def __init__(self, path: Path):
        self._path = path

    @property
    def name(self) -> str:
        return self._path.stem

    @property
    def filetype(self) -> str:
        ext = self._path.suffix[1:]
        if ext:
            return ext
        try:
            with open(self._path) as script:
                line = script.readline()
                if line.startswith("#!"):
                    return line.split(" ")[1].rstrip()
        except UnicodeDecodeError:
            pass
        return BrightColor.fg("Red") + "??" + Color.reset()

    def num_lines(self) -> typing.Tuple[int, int]:
        line_count = 0
        blank_line_count = 0
        try:
            for line in self._path.open():
                line_count += 1
                if not line.strip():
                    blank_line_count += 1
            return line_count, blank_line_count
        except UnicodeDecodeError:
            return -1, 0

    def to_str(self) -> str:
        num_lines = self.num_lines()
        return (
            f"{self.name} ".ljust(20, ".")
            + "  [ "
            + self.filetype.center(8)
            + " ]   "
            + str(num_lines[0]).rjust(4)
            + " lines .... "
            + str(num_lines[1]).rjust(3)
            + " blank | "
            + str(num_lines[0] - num_lines[1]).rjust(3)
            + "  LoC"
        )


class ScriptsHome:
    @property
    def script_dir(self) -> Path:
        """Gets the path to the script-directory home."""
        return Path.home().joinpath("bin")

    def setUp(self):
        """Creates scripts home, if it doesn't already exist."""
        home_folder = self.script_dir
        if not home_folder.exists():
            print(f"Creating scripts home directory: {home_folder}")
            home_folder.mkdir()

    def scripts(self):
        return [
            ScriptFile(script)
            for script in self.script_dir.iterdir()
            if script.is_file()
        ]


print(
    " IDX |   Executable Name    ~    File Type ~   Number of Lines  ( Blank //  LoC  )"
)
print("=" * 82)
for idx, script in enumerate(ScriptsHome().scripts(), start=1):
    print(f" {str(idx).rjust(2)}  -   {script.to_str()}")
