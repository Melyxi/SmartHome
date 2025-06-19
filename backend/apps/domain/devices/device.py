from apps.domain.buttons.button import ButtonService
from apps.domain.devices.exceptions import DeviceNotFoundError
from apps.domain.exceptions import ButtonsNotFoundValidationError
from apps.domain.utils import populate_buttons
from apps.models.device import GetDevice, PostDevice, PutDevice
from apps.repositories.protocol import ProtocolSqlAlchemyRepository
from core.enums import ProtocolType
from core.models.device import Device
from core.repositories.base.decorators import validate_db_error
from core.repositories.base.exceptions import ModelNotFoundError
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

    async def get(self, _id: int):
        device = await self.repository.get_device_and_protocol_with_buttons_and_meta_with_states_by_id(_id)
        if not device:
            raise DeviceNotFoundError
        await self.build_html(device)
        return self.get_model.model_validate(device, from_attributes=True), 200

    @validate_db_error
    async def create(self, device: PostDevice):
        device_dict = device.model_dump()
        await self.validate_post()
        device = await self.repository.create(**device_dict)
        return {"device": device.id}, 201

    @validate_db_error
    async def update(self, _id: int, device: PutDevice):
        self._properties = device.model_dump(exclude_unset=True)
        self._model_id = _id
        await self.validate_update()
        try:
            device = await self.repository.update(self._model_id, **self._properties)
        except ModelNotFoundError:
            raise DeviceNotFoundError

        return {"device": device.id}, 200

    async def validate_update(self):
        # Validate model exists
        button_ids = self._properties.get("buttons")

        #Validate/Populate buttons
        try:
            if button_ids:
                buttons = await populate_buttons(button_ids)
                self._properties["buttons"] = buttons
        except ButtonsNotFoundValidationError:
            raise ButtonsNotFoundValidationError


    async def validate_post(self):
        if not self._properties["html"]:
            protocol = await ProtocolSqlAlchemyRepository(self.repository.session).get_by_id(self._properties["protocol_id"])
            if protocol.type is ProtocolType.ZIGBEE:
                self._properties["html"] = mqtt_device_html
            else:
                self._properties["html"] = device_html

        self._properties["buttons"] = await populate_buttons(self._properties["buttons"])

        if not self._properties["unique_name"]:
            self._properties["unique_name"] = str(self._properties["uuid"])

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
