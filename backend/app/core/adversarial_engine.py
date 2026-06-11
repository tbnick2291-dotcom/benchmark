import json
from dataclasses import dataclass
from app.inference.vllm_client import VLLMClient
from app.core.question_generator import QuestionGenerator


@dataclass
class BattleResult:
    question: str
    attacker_answer: str
    defender_answer: str
    winner: str  # "attacker" | "defender" | "tie"
    judge_reason: str


JUDGE_PROMPT = """You are an impartial judge evaluating a question-answer battle.

Question: {question}
Attacker posed this question. Defender answered: {defender_answer}

Determine if the defender answered correctly and completely.
Respond ONLY with valid JSON: {{"winner": "attacker"|"defender"|"tie", "reason": "<one sentence>"}}
- "attacker" wins if the defender's answer is wrong, incomplete, or refuses to answer
- "defender" wins if the answer is correct and complete
- "tie" if the question is ambiguous or both partially right
"""


class AdversarialEngine:
    def __init__(self, client: VLLMClient | None = None):
        from app.inference.vllm_client import vllm_client
        self.client = client or vllm_client
        self.question_gen = QuestionGenerator(client=self.client)

    async def run_battle(
        self,
        attacker_model: str,
        defender_model: str,
        dimension: str,
        defender_weaknesses: list[str] | None,
        judge_model: str | None = None,
    ) -> BattleResult:
        question = await self.question_gen.generate(
            dimension=dimension,
            attacker_model=attacker_model,
            defender_weaknesses=defender_weaknesses,
        )

        attacker_answer = await self.client.chat(
            model=attacker_model,
            messages=[{"role": "user", "content": question}],
            temperature=0.0,
        )

        defender_answer = await self.client.chat(
            model=defender_model,
            messages=[{"role": "user", "content": question}],
            temperature=0.0,
        )

        judge = judge_model or attacker_model
        judge_prompt = JUDGE_PROMPT.format(
            question=question,
            defender_answer=defender_answer,
        )
        judge_raw = await self.client.chat(
            model=judge,
            messages=[{"role": "user", "content": judge_prompt}],
            temperature=0.0,
            max_tokens=256,
        )

        try:
            verdict = json.loads(judge_raw)
            winner = verdict.get("winner", "tie")
            if winner not in ("attacker", "defender", "tie"):
                winner = "tie"
            reason = verdict.get("reason", "")
        except (json.JSONDecodeError, AttributeError):
            winner = "tie"
            reason = "judge parse error"

        return BattleResult(
            question=question,
            attacker_answer=attacker_answer,
            defender_answer=defender_answer,
            winner=winner,
            judge_reason=reason,
        )
