"""Configuration loader using Dynaconf."""

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="RAG",
    settings_files=["configs/settings.yaml", "configs/.secrets.yaml"],
    environments=True,
    load_dotenv=True,
)
