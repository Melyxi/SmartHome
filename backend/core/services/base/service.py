from core.types import R


class BaseService:
    def __init__(self, repository: R):
        self.repository = repository
