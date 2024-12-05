from enum import StrEnum
from pathlib import Path

import click
import tomllib

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


class TemplateEnum(StrEnum):
    PYTHON = "python"


@click.group()
def template():
    pass


@template.command()
def list():
    for template in TEMPLATE_DIR.iterdir():
        print(template.name)


@template.command()
@click.argument("template", type=click.Choice(TemplateEnum))
def get(template: TemplateEnum):
    path = (TEMPLATE_DIR / template.value).with_suffix(".toml")
    settings = tomllib.loads(path.read_text())
    print(settings)
