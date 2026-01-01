import json
from pathlib import Path
from uuid import uuid4

from exceptions import ModuleUUIDNotFoundError, UUIDFileNotFoundError
from weather_api import JSON_FILE_PATH, UUID_FILE_PATH, default_setting
from weather_api.exposes import ExposesManager


class RegistrationManager:
    filename = Path(__file__).parent / ".uuid"

    def __init__(self):
        self.module_uuid = None

    @staticmethod
    def create_module_uuid() -> None:
        if not Path(UUID_FILE_PATH).exists():
            with open(UUID_FILE_PATH, "w") as f:
                f.write(str(uuid4()))

    def initialization_uuid(self) -> None:
        if Path(UUID_FILE_PATH).exists():
            with open(UUID_FILE_PATH) as f:
                module_uuid = f.readline()
                if module_uuid:
                    self.module_uuid = module_uuid
                else:
                    raise ModuleUUIDNotFoundError(f"Not found uuid in file {UUID_FILE_PATH}")
        else:
            raise UUIDFileNotFoundError(f"Not found file with uuid. {UUID_FILE_PATH}")

    @staticmethod
    def create_json_file() -> None:
        if not JSON_FILE_PATH.exists():
            with open(JSON_FILE_PATH, "w") as f:
                json.dump(default_setting, f, ensure_ascii=False, indent=4)

    def registration(self) -> dict[str, str]:
        self.create_module_uuid()
        self.initialization_uuid()
        self.create_json_file()

        exposes_manager = ExposesManager()
        exposes = exposes_manager.get_exposes()

        return {
            "unique_name": self.module_uuid,
            "uuid": self.module_uuid,
            "exposes": json.dumps(exposes),
            "name": "Weather",
        }


module_registration = RegistrationManager().registration
