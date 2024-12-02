from scaffolding.core.blueprint import Blueprint
from scaffolding.core.interfaces.language import Language, LanguageBuilder, Python


def test_language(blueprint: Blueprint):
    # create the folder cause the create_directory method is mocked
    blueprint.folder.mkdir(parents=True, exist_ok=False)

    language = Language(blueprint.folder)
    assert language.cwd == blueprint.folder


def test_python_language(blueprint: Blueprint):
    # create the folder cause the create_directory method is mocked
    blueprint.folder.mkdir(parents=True, exist_ok=False)

    language = Python(blueprint.folder)
    assert language.cwd == blueprint.folder


def test_language_builder(blueprint: Blueprint):
    # create the folder cause the create_directory method is mocked
    blueprint.folder.mkdir(parents=True, exist_ok=False)

    builder = LanguageBuilder(blueprint)
    builder.build()
