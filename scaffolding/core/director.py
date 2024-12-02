from .factory import ProjectFactory


class ProjectDirector:
    def __init__(self, factory: ProjectFactory) -> None:
        self.factory = factory

    def process(self) -> None:
        self.factory.create_project()
        self.factory.create_language()
        self.factory.create_license()
        self.factory.create_git()
