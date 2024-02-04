from pathlib import Path
import sys

from .utils import getch

INFO_DIR = Path(__file__).parent / "sections"


def clear():
    print("\033c", end="")


def usage():
    print(f"Usage:\n\tadvik [section1] [section2] ...")
    print(f"Sections:\n\t{', '.join([f.stem for f in INFO_DIR.iterdir()])}")


def print_section(section):
    file = INFO_DIR / section
    if file.exists():
        print(file.read_text())


def interactive():
    sections = [f.stem for f in INFO_DIR.iterdir()]
    current = 0

    key = ""
    while key != "q":
        if key == "n":
            current += 1
        elif key == "p":
            current -= 1

        clear()
        print_section(sections[current % len(sections)])
        print("(n)ext section, (p)revious section, (h)elp, (q)uit")
        key = getch()


def main():
    if len(sys.argv) == 1:
        interactive()
    elif sys.argv[1] in ["-h", "--help"]:
        usage()
    else:
        sections = sys.argv[1:]
        for section in sections:
            print_section(section)


# Show an easter egg if the user tries to import the package.
if __name__ != "advik":
    print("Why are you importing me?")
