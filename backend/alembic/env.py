import os
import sys
from logging.config import fileConfig

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from alembic import context

# from backend.configs.config import settings
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.insert(0, project_root)
sys.path.insert(0, f"{project_root}/backend")
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from configs.config import settings
from core.models import account, association, button, device, meta_button, protocol, state, scene

targets_metadata = [
    account.User.metadata,
    protocol.Protocol.metadata,
    state.State.metadata,
    meta_button.MetaButton.metadata,
    button.Button.metadata,
    button.button_state_association.metadata,
    association.device_button_association.metadata,
    device.Device.metadata,
    scene.Scene.metadata
]

# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
# DATABASE_URL = config.get_main_option("DATABASE_URL")
DATABASE_URL = settings.get("DATABASE_URL")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")

    for target_metadata in targets_metadata:
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()


async_engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))

    for target_metadata in targets_metadata:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,  # Replace with your actual target metadata
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()