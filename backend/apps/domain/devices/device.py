from apps.domain.buttons.button import ButtonService
from apps.domain.utils import populate_buttons
from apps.models.device import GetDevice, PostDevice
from apps.repositories.protocol import ProtocolSqlAlchemyRepository
from core.enums import ProtocolType
from core.models.device import Device
from core.services.base.service import BaseService
from core.templates import device_html, mqtt_device_html
from jinja2 import Template
from simplejson import JSONDecodeError
from utils import json


class DeviceService(BaseService):
    get_model = GetDevice

    async def list_devices(self):
        devices = await self.repository.get_device_and_protocol_with_buttons_and_meta_with_states()
        response = []
        for device in devices:
            await self.build_html(device)
            response.append(self.get_model.model_validate(device, from_attributes=True))
        return response, 200

    async def post(self, device: PostDevice):
        device_dict = device.model_dump()
        await self.validate_post(device_dict)
        device = await self.repository.create(**device_dict)
        return {"device": device.id}, 201


    async def validate_post(self, device: dict):
        if not device["html"]:
            protocol = await ProtocolSqlAlchemyRepository(self.repository.session).get_by_id(device["protocol_id"])
            if protocol.type is ProtocolType.ZIGBEE:
                device["html"] = mqtt_device_html
            else:
                device["html"] = device_html

        device["buttons"] = await populate_buttons(device["buttons"])

        if not device["unique_name"]:
            device["unique_name"] = str(device["uuid"])

    @staticmethod
    def get_exposes(model):
        try:
            exposes =  json.loads(model.exposes)
        except JSONDecodeError:
            exposes = []

        return exposes

    @classmethod
    async def build_html(cls, _model: Device, context=None):
        if context is None:
            context = {}

        context["device"] = _model

        exposes = cls.get_exposes(_model)
        context["exposes"] = exposes
        _model.exposes = exposes

        for button in _model.buttons:
            await ButtonService.build_html(_model=button, context=context)

        html = Template(_model.html).render(**context)

        _model.html = html
        return html
