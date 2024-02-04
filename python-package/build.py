from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from yaml import safe_load

from pathlib import Path
import sys

WIDTH = 60


class DotAccess(dict):
    def __getattr__(self, k):
        v = self[k]
        if isinstance(v, dict):
            return DotAccess(v)
        if isinstance(v, (list, tuple, set)):
            return [DotAccess(x) if isinstance(x, dict) else x for x in v]
        return v


def create_panel(title, content):
    return Panel(
        content, title=f"[b red]{title}", border_style="blue", width=WIDTH, padding=0
    )


def get_about_me(info):
    contact = Table.grid(padding=(0, 4))
    contact.add_row(
        ":telephone_receiver: [b green]Phone", f"[b yellow]{info.personal.phone}"
    )
    contact.add_row(":e-mail: [b green]Email", f"[b yellow]{info.personal.email}")
    contact.add_row(
        ":link: [b green]Github",
        f"[b yellow][link={info.personal.github}]{info.personal.github}[/link]",
    )
    contact.add_row(
        ":link: [b green]LinkedIn",
        f"[b yellow][link={info.personal.linkedin}]{info.personal.linkedin}[/link]",
    )

    return create_panel(
        "About Me",
        Group(
            f"Hi, I'm [b green]{info.personal.name}[/b green] :wave:\n",
            "I'm a [b green]Python Developer[/b green] :snake: who loves to build things.",
            "I built this resume using [b green]Python[/b green] and [b green]Rich[/b green].",
            "I'm looking for a [b green]remote[/b green] job.\n",
            contact,
        ),
    )


def get_experience(info):
    experience = Table.grid(expand=True, padding=(0, 4))
    experience.add_column(justify="left")
    experience.add_column(justify="right")

    for i, job in enumerate(info.experience):
        experience.add_row(
            f":briefcase: [b green]{job.role}[/b green]", f"{job.date} :date:"
        )
        experience.add_row(
            f":office: [i yellow]{job.name}[/i yellow]",
            f"[i]{job.location} :round_pushpin:",
        )
        for point in job.points or []:
            experience.add_row(f"  [b yellow]•[/b yellow] {point}")

        if i < len(info.experience) - 1:
            experience.add_row()

    return create_panel("Experience", experience)


def get_projects(info):
    projects = Table.grid(expand=True, padding=(0, 4))
    projects.add_column(justify="left", no_wrap=True)
    projects.add_column(justify="right", no_wrap=True)

    for i, project in enumerate(info.projects):
        projects.add_row(f":rocket: [b green]{project.name}[/b green]")
        projects.add_row(f":star: [i yellow]{project.skills}[/i yellow]")
        for point in project.points or []:
            projects.add_row(f"  [b yellow]•[/b yellow] {point}")

        if i < len(info.projects) - 1:
            projects.add_row()

    return create_panel("Projects", projects)


def get_education(info):
    school = info.education[0]
    education = Table.grid(expand=True, padding=(0, 4))

    education.add_row(f":graduation_cap: [b green]{school.name}[/b green]")
    education.add_row(f":books: [i yellow]{school.degree}[/i yellow]")
    education.add_row(f":date: [i]{school.date}[/i]")
    education.add_row(f":round_pushpin: [i]{school.location}[/i]")

    return create_panel("Education", education)


def get_skills(info):
    skills = Table.grid(expand=True, padding=(0, 4))
    for i, skill in enumerate(info.skills):
        skills.add_row(f"[b green]{skill.category}[/b green]")
        skills.add_row(f":star: [i yellow]{skill.skills}[/i yellow]")

        if i < len(info.skills) - 1:
            skills.add_row()

    return create_panel("Skills", skills)


def build_resume(info, output_dir):
    console = Console(record=True)
    for section, panel in [
        ("1-about", get_about_me(info)),
        ("2-experience", get_experience(info)),
        ("3-projects", get_projects(info)),
        ("4-education", get_education(info)),
        ("5-skills", get_skills(info)),
    ]:
        # console.clear()
        console.print(panel)
        console.save_text(str(output_dir / section), styles=True)


def main():
    if len(sys.argv) != 3:
        print("Usage:\n\tpython build.py <input_file> <output_dir>")
        sys.exit(1)

    INPUT_FILE = Path(sys.argv[1])
    if not INPUT_FILE.exists():
        print(f"File not found: {INPUT_FILE}")
        sys.exit(1)

    OUTPUT_DIR = Path(sys.argv[2])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load the resume data from the YAML file
    with open(INPUT_FILE) as file:
        info = DotAccess(safe_load(file))
        build_resume(info, OUTPUT_DIR)


if __name__ == "__main__":
    main()
