import httpx
import sys
from rich.console import Console

console = Console(stderr=True)


def get(url: str, base_url: str) -> dict | list:
    try:
        r = httpx.get(f"{base_url}/api/v1{url}", timeout=30)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        console.print(f"[red]Error {e.response.status_code}:[/red] {e.response.text}")
        sys.exit(1)
    except httpx.RequestError as e:
        console.print(f"[red]Connection error:[/red] {e}")
        sys.exit(1)


def post(url: str, base_url: str, json: dict | None = None) -> dict:
    try:
        r = httpx.post(f"{base_url}/api/v1{url}", json=json, timeout=30)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        console.print(f"[red]Error {e.response.status_code}:[/red] {e.response.text}")
        sys.exit(1)
    except httpx.RequestError as e:
        console.print(f"[red]Connection error:[/red] {e}")
        sys.exit(1)


def patch(url: str, base_url: str, json: dict) -> dict:
    try:
        r = httpx.patch(f"{base_url}/api/v1{url}", json=json, timeout=30)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        console.print(f"[red]Error {e.response.status_code}:[/red] {e.response.text}")
        sys.exit(1)
    except httpx.RequestError as e:
        console.print(f"[red]Connection error:[/red] {e}")
        sys.exit(1)
