from core.types import R


class BaseService:
    def __init__(self, repository: R):
        self.repository = repository
        self._properties: dict = {}
        self._model_id: int | None = None
        self._model = None
