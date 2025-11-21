from typing import Any

from apps.domain.mqtt.cache import MqttCacheManager
from apps.models.history import ColumnPropertiesSchema, HistoryDataQuerySchema, HistoryDataResponseSchema
from core.extensions import cache as backend_cache
from core.services.base.service import BaseService
from utils import json


class HistoryService(BaseService):
    cache = backend_cache

    @staticmethod
    async def _pure_exposes(exposes: list[Any]):
        remove_expose = []
        add_features = []

        for expose in exposes:
            if features := expose.get("features"):
                remove_expose.append(expose)
                add_features.append(features)

        for expose in remove_expose:
            exposes.remove(expose)

        for feature in add_features:
            exposes.extend(feature)
        return exposes

    async def __prepare_devices(self, device_exposes):
        prepared_devices_exposes = {}
        for device in device_exposes:
            prepared_devices_exposes[device["unique_name"]] = await self._pure_exposes(json.loads(device["exposes"]))
        return prepared_devices_exposes

    async def get_history(self, device_name: str, row_count: int | None = None):
        device_data = await MqttCacheManager(self.cache).get_history_by_device(device_name)
        history = device_data["history"]

        if row_count is None or row_count > 1000:
            row_count = 1000

        history = dict(zip(list(history.keys())[-row_count:], list(history.values())[-row_count:]))
        return history

    @staticmethod
    async def _prepared_filters(query_filters: list[str]):
        return [_filter.split(".") for _filter in query_filters]

    @staticmethod
    async def apply_filters(value: dict, prepared_filters: list[list[str]]):
        if prepared_filters:
            filtered_data = {}

            for _filter in prepared_filters:
                contained_filed = ""
                process_data = value
                for filed in _filter:
                    process_data = process_data[filed]
                    contained_filed += filed + " "

                filtered_data[contained_filed.strip()] = process_data
            return filtered_data

        return value

    async def get_detailed_info(
        self, exposes: list[dict[str, Any]], query_filters: list[str]
    ) -> list[ColumnPropertiesSchema]:
        prepared_filters = await self._prepared_filters(query_filters)
        if prepared_filters:
            detailed_info = []
            for _filter in prepared_filters:
                for field in exposes:
                    if field["property"] in _filter:
                        detailed_info.append(ColumnPropertiesSchema(**field))
            return detailed_info
        return [ColumnPropertiesSchema(**field) for field in exposes]

    async def get_history_data(self, queries: HistoryDataQuerySchema) -> list[HistoryDataResponseSchema]:
        devices = [query.device_unique_name for query in queries.queries]
        device_exposes = await self.repository.get_devices_expose_by_names(devices)

        prepared_devices_exposes = await self.__prepare_devices(device_exposes)

        result = []

        for query in queries.queries:
            data = []
            prepared_filters = await self._prepared_filters(query.fields)
            history = await self.get_history(query.device_unique_name, query.row_limit)
            filtered_value = {}
            for time, value in history.items():
                filtered_value = await self.apply_filters(value, prepared_filters)
                filtered_value.update({"time": time})

                data.append(filtered_value)

            detailed_information = await self.get_detailed_info(
                prepared_devices_exposes[query.device_unique_name], query.fields
            )
            result.append(
                HistoryDataResponseSchema(
                    **{
                        "data": data,
                        "colnames": list(filtered_value.keys()),
                        "detailed_information": detailed_information,
                        "rowcount": query.row_limit,
                        "result_format": "JSON",
                    }
                )
            )
        return result
