import click

from .project import project
from .template import template

cli = click.CommandCollection(sources=[project, template])
