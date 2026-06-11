import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


def test_task_list(runner):
    # 直接测试 task group，不通过 cli 主入口（避免 main.py 冲突）
    from benchmark_cli.commands.task import group
    mock_tasks = [{"id": 1, "name": "k-battle", "dimension": "knowledge", "status": "pending", "created_at": "2026-01-01T00:00:00", "completed_at": None}]
    with patch("benchmark_cli.commands.task.api_get", return_value=mock_tasks):
        # 需要提供 obj（Context）
        from benchmark_cli.main import Context
        result = runner.invoke(group, ["list"], obj=Context("http://localhost:8080"))
    assert result.exit_code == 0
    assert "k-battle" in result.output


def test_task_create(runner):
    from benchmark_cli.commands.task import group
    mock_task = {"id": 2, "name": "new", "dimension": "code", "status": "pending", "created_at": "2026-01-01T00:00:00", "completed_at": None}
    with patch("benchmark_cli.commands.task.api_post", return_value=mock_task):
        from benchmark_cli.main import Context
        result = runner.invoke(group, ["create", "new", "--dimension", "code", "--models", "1,2", "--rounds", "3"], obj=Context("http://localhost:8080"))
    assert result.exit_code == 0
    assert "new" in result.output


def test_task_start(runner):
    from benchmark_cli.commands.task import group
    mock_task = {"id": 1, "name": "t", "dimension": "knowledge", "status": "running", "created_at": "2026-01-01T00:00:00", "completed_at": None}
    with patch("benchmark_cli.commands.task.api_post", return_value=mock_task):
        from benchmark_cli.main import Context
        result = runner.invoke(group, ["start", "1"], obj=Context("http://localhost:8080"))
    assert result.exit_code == 0
