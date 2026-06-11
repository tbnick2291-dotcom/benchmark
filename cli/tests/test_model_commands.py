import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from click.testing import CliRunner
from benchmark_cli.main import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_model_list_displays_table(runner):
    mock_models = [{"id": 1, "name": "llama3", "model_path": "/models/llama3", "status": "active", "created_at": "2026-01-01T00:00:00"}]
    with patch("benchmark_cli.commands.model.api_get", return_value=mock_models):
        result = runner.invoke(cli, ["model", "list"])
    assert result.exit_code == 0
    assert "llama3" in result.output
    assert "active" in result.output


def test_model_register(runner):
    mock_model = {"id": 2, "name": "new-model", "model_path": "/p", "status": "inactive", "created_at": "2026-01-01T00:00:00"}
    with patch("benchmark_cli.commands.model.api_post", return_value=mock_model):
        result = runner.invoke(cli, ["model", "register", "new-model", "/p"])
    assert result.exit_code == 0
    assert "new-model" in result.output


def test_model_load(runner):
    mock_model = {"id": 1, "name": "m", "model_path": "/p", "status": "active", "created_at": "2026-01-01T00:00:00"}
    with patch("benchmark_cli.commands.model.api_patch", return_value=mock_model):
        result = runner.invoke(cli, ["model", "load", "1"])
    assert result.exit_code == 0
    assert "active" in result.output
