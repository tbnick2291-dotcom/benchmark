import httpx
from app.config import settings


class VLLMClient:
    """Wraps vLLM's OpenAI-compatible /v1/chat/completions endpoint."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.vllm_base_url

    async def chat(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def list_models(self) -> list[str]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/models")
            response.raise_for_status()
            data = response.json()
            return [m["id"] for m in data.get("data", [])]


vllm_client = VLLMClient()
