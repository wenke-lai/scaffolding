import structlog

from .factory import ProjectFactory

logger = structlog.get_logger(__name__)


class ProjectDirector:
    def __init__(self, factory: ProjectFactory) -> None:
        self.factory = factory

    def process(self) -> None:
        logger.debug("director process")
        self.factory.create_project()
        self.factory.create_language()
        self.factory.create_license()
        self.factory.create_git()
