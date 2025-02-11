from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
import models
from alembic import context

# Alembic yapılandırmasını al
config = context.config
fileConfig(config.config_file_name)

# SQLAlchemy modellerinin metadata bilgisini al
target_metadata = models.Base.metadata

def run_migrations_offline() -> None:
    """Veritabanı migrasyonlarını 'offline' modda çalıştırır."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata,
        literal_binds=True, dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Veritabanı migrasyonlarını 'online' modda çalıştırır."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.", poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
