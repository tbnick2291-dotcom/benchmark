import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import AsyncMock, patch
from app.core.question_generator import QuestionGenerator, DIMENSION_PROMPTS


def test_dimension_prompts_exist():
    for dim in ["knowledge", "reasoning", "code", "safety"]:
        assert dim in DIMENSION_PROMPTS
        assert len(DIMENSION_PROMPTS[dim]) > 20


@pytest.mark.asyncio
async def test_generate_returns_string():
    gen = QuestionGenerator()
    mock_response = "What is the capital of France?"
    with patch.object(gen.client, "chat", new=AsyncMock(return_value=mock_response)):
        result = await gen.generate(
            dimension="knowledge",
            attacker_model="test-model",
            defender_weaknesses=None,
        )
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_generate_includes_weakness_in_prompt():
    gen = QuestionGenerator()
    captured_messages = []

    async def mock_chat(model, messages, **kwargs):
        captured_messages.extend(messages)
        return "tricky question"

    with patch.object(gen.client, "chat", new=mock_chat):
        await gen.generate(
            dimension="reasoning",
            attacker_model="test-model",
            defender_weaknesses=["multi-step logic"],
        )
    prompt_text = " ".join(m["content"] for m in captured_messages)
    assert "multi-step logic" in prompt_text
