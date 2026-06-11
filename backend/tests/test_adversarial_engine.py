import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import AsyncMock, patch
from app.core.adversarial_engine import AdversarialEngine, BattleResult


@pytest.fixture
def engine():
    return AdversarialEngine()


@pytest.mark.asyncio
async def test_battle_result_has_required_fields(engine):
    with patch.object(engine.question_gen, "generate", new=AsyncMock(return_value="Test question?")):
        with patch.object(engine.client, "chat", new=AsyncMock(side_effect=["Attacker answer", "Defender answer", '{"winner": "defender", "reason": "correct"}'])):
            result = await engine.run_battle(
                attacker_model="model_a",
                defender_model="model_b",
                dimension="knowledge",
                defender_weaknesses=None,
            )
    assert isinstance(result, BattleResult)
    assert result.question is not None
    assert result.attacker_answer is not None
    assert result.defender_answer is not None
    assert result.winner in ("attacker", "defender", "tie")


@pytest.mark.asyncio
async def test_battle_winner_parsed_from_judge(engine):
    with patch.object(engine.question_gen, "generate", new=AsyncMock(return_value="Q?")):
        with patch.object(engine.client, "chat", new=AsyncMock(side_effect=["attacker_ans", "defender_ans", '{"winner": "attacker", "reason": "wrong answer"}'])):
            result = await engine.run_battle("a", "b", "knowledge", None)
    assert result.winner == "attacker"


@pytest.mark.asyncio
async def test_battle_defaults_to_tie_on_bad_judge_response(engine):
    with patch.object(engine.question_gen, "generate", new=AsyncMock(return_value="Q?")):
        with patch.object(engine.client, "chat", new=AsyncMock(side_effect=["ans1", "ans2", "not valid json"])):
            result = await engine.run_battle("a", "b", "knowledge", None)
    assert result.winner == "tie"
