from apps.domain.buttons.button import ButtonService
from apps.models.device import GetDevice
from core.models.device import Device
from core.services.base.service import BaseService
from jinja2 import Template


class DeviceService(BaseService):
    get_model = GetDevice

    async def list_devices(self):
        devices = await self.repository.get_device_and_protocol_with_buttons_and_meta_with_states()
        response = []
        for device in devices:
            await self.build_html(device)
            response.append(self.get_model.from_orm(device))
        return response, 200

    @classmethod
    async def build_html(cls, _model: Device, context=None):
        if context is None:
            context = {}

        context["device"] = _model

        for button in _model.buttons:
            await ButtonService.build_html(_model=button, context=context)

        html = Template(_model.html).render(**context)

        _model.html = html
        return  html



