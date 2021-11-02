#!/usr/bin/env python3

from pathlib import Path
import typing


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
        return "??"

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
