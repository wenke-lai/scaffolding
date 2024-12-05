from ..managers import GitManager
from .builder import Builder


class GitBuilder(Builder):
    def __init__(self):
        self.git = GitManager()

    def create_initial_commit(self):
        self.git.add()
        self.git.commit("feat: initial project")
