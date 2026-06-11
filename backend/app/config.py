from pydantic_settings import BaseSettings
import yaml
from pathlib import Path


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://benchmark:benchmark@localhost:5432/benchmark"
    vllm_base_url: str = "http://localhost:8000/v1"
    elo_k_factor: float = 32.0
    elo_initial_rating: float = 1500.0
    debug: bool = False

    model_config = {"env_prefix": "BENCHMARK_", "extra": "ignore"}


def load_settings(config_path: str = "config/config.yaml") -> Settings:
    path = Path(config_path)
    overrides = {}
    if path.exists():
        with open(path) as f:
            overrides = yaml.safe_load(f) or {}
    return Settings(**overrides)


settings = load_settings()
