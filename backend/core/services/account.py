from backend.core.repositories.base.base import SqlRepositoryAbstract


class AccountService:
    def __init__(self, repository: SqlRepositoryAbstract):
        self.repository = repository

    async def login(self):
        pass

    async def registration(self):
        pass
