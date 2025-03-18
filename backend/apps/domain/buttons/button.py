from core.models.button import Button
from core.models.meta_button import MetaButton
from core.services.base.service import BaseService
from jinja2 import Template

class ButtonService(BaseService):

    @classmethod
    async def build_html(cls, _model: Button, context=None):
        """
        :param context:
        :param _model:
        :return:
        """
        if context is None:
            context = {}
        context["button"] = _model
        meta_button = _model.meta_button
        return await MetaButtonService.build_html(meta_button, context=context)


class MetaButtonService(BaseService):

    @classmethod
    async def build_html(cls, _model: MetaButton, context=None):
        """
        :param context:
        :param _model:
        :return:

        Build html for button
            button - html
               button_meta - html
        """

        if context is None:
            context = {}

        html = Template(_model.html).render(**context)
        _model.html = html

        return html
