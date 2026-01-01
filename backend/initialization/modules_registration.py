import importlib
import sys
from pathlib import Path

from core.configurate_logging import get_logger
from core.enums import ProtocolType
from core.models.device import Device
from core.models.protocol import Protocol
from extensions import db
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

server_logger = get_logger("server")


class ModuleRegistry:
    custom_modules_path = Path(__file__).parent.parent / "custom_modules"

    @classmethod
    def add_module_path(cls) -> None:
        if cls.custom_modules_path.exists():
            sys.path.insert(0, str(cls.custom_modules_path))
            for item in cls.custom_modules_path.iterdir():
                module_name = item.name
                if item.is_dir() and not item.name.startswith(".") and "__pycache__" not in module_name:
                    module_path = str(Path(cls.custom_modules_path, module_name))
                    if module_path not in sys.path:
                        sys.path.insert(0, module_path)

    @classmethod
    def discover_modules_registration(cls):
        """
        Обнаруживает и регистрирует все модули в custom_modules
        """
        registered_modules = {}
        if not cls.custom_modules_path.exists():
            return registered_modules

        for item in cls.custom_modules_path.iterdir():
            module_name = item.name
            if item.is_dir() and not item.name.startswith(".") and "__pycache__" not in module_name:
                try:
                    module = importlib.import_module(f"custom_modules.{module_name}.registration")
                    if hasattr(module, "module_registration"):
                        module_registration = module.module_registration

                        try:
                            registration_result = module_registration()
                            registered_modules[module_name] = registration_result

                        except Exception as e:
                            server_logger.error("Error executing module_registration for {}: {}", module_name, e)

                except ImportError as e:
                    server_logger.error("Failed to import module {}.registration: {}", module_name, e)

                except Exception as e:
                    server_logger.error("Error processing module {}: {}", module_name, e)

        return registered_modules

    def create_modules(self):
        modules = self.discover_modules_registration()

        for module in modules.values():
            try:
                with db.sync_session() as session:
                    protocol = session.execute(select(Protocol).filter_by(type=ProtocolType.MODULE.value)).scalar()
                    module.update({"protocol_id": protocol.id})
                    device_object = Device(**module)
                    session.add(device_object)
                    session.flush()
                    session.commit()
                    server_logger.info("Success add {} module", module["name"])

            except IntegrityError:
                session.rollback()

    @classmethod
    def discover_modules_tasks(cls):
        cls.add_module_path()
        startup_tasks = []
        shutdown_tasks = []
        if not cls.custom_modules_path.exists():
            return startup_tasks, shutdown_tasks

        for item in cls.custom_modules_path.iterdir():
            module_name = item.name
            if item.is_dir() and not item.name.startswith(".") and "__pycache__" not in module_name:
                module_name = item.name
                try:
                    module = importlib.import_module(f"custom_modules.{module_name}.tasks")

                    if hasattr(module, "startup_event"):
                        try:
                            startup_tasks.append(module.startup_event)

                        except Exception as e:
                            server_logger.error("Error executing startup_event for {}: {}", module_name, e)
                    if hasattr(module, "shutdown_event"):
                        try:
                            shutdown_tasks.append(module.shutdown_event)

                        except Exception as e:
                            server_logger.error("Error executing shutdown_event for {}: {}", module_name, e)

                except ImportError as e:
                    server_logger.error("Failed to import module {}.tasks: {}", module_name, e)

                except Exception as e:
                    server_logger.error("Error processing module {}: {}", module_name, e)

        return startup_tasks, shutdown_tasks

    @classmethod
    def get_tasks(cls):
        cls.add_module_path()
        return cls.discover_modules_tasks()
