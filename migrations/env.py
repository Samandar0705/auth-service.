from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Bu qism Alembic tomonidan avtomatik yaratiladi
config = context.config

# Log sozlamalari
fileConfig(config.config_file_name)

# Bizning modellarimizni import qilamiz
from app.models.base import Base
from app.models.user import User
from app.models.role import Role

# MetaData'ni sozlash
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()