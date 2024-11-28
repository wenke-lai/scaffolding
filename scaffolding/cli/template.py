from enum import StrEnum

import tomllib
import typer

from scaffolding.cli.constant import TEMPLATE_SUFFIX, TEMPLATES

app = typer.Typer()


class Template(StrEnum):
    PYTHON = "python"


def load_template(template: Template) -> dict:
    path = (TEMPLATES / template.value).with_suffix(TEMPLATE_SUFFIX)
    with open(path, "rb") as fr:
        return tomllib.load(fr)


@app.command()
def get(template: Template, to_file: bool = False):
    path = (TEMPLATES / template.value).with_suffix(TEMPLATE_SUFFIX)
    assert path.is_file(), f"Template {template.value} not found"
    with open(path, "r", encoding="utf-8") as fr:
        if to_file:
            with open(f"template-{template.value}.toml", "w", encoding="utf-8") as fw:
                fw.write(fr.read())
        else:
            print(fr.read())


@app.command()
def check(template: Template):
    pass
