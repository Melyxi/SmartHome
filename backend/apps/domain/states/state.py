from apps.models.state import GetState
from core.services.base.service import BaseService


class StateService(BaseService):
    get_model = GetState

    async def get(self, _id: int):
        state = await self.repository.get_by_id(_id)
        response = self.get_model.model_validate(state)
        return response, 200
