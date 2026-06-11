from pydantic_settings import BaseSettings
import yaml
from pathlib import Path

# 相对于 config.py 本身定位项目根目录：backend/app/config.py → ../../ → 项目根
_DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "config.yaml"


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://benchmark:benchmark@localhost:5432/benchmark"
    vllm_base_url: str = "http://localhost:8000/v1"
    elo_k_factor: float = 32.0
    elo_initial_rating: float = 1500.0
    debug: bool = False

    model_config = {"env_prefix": "BENCHMARK_", "extra": "ignore"}


def load_settings(config_path: Path = _DEFAULT_CONFIG_PATH) -> Settings:
    overrides = {}
    if config_path.exists():
        with open(config_path) as f:
            overrides = yaml.safe_load(f) or {}
    return Settings(**overrides)


settings = load_settings()
