import click
from rich.table import Table
from rich.console import Console
from benchmark_cli.client import get as api_get

console = Console()


@click.command()
@click.pass_obj
def command(ctx):
    """Show system status"""
    health = api_get("/system/health", ctx.url)
    status = api_get("/system/status", ctx.url)
    console.print(f"API: [green]{health['status']}[/green]")
    vllm = status['vllm_status']
    color = 'green' if vllm == 'online' else 'red'
    console.print(f"vLLM: [{color}]{vllm}[/{color}]")
    if status.get("loaded_models"):
        table = Table(title="Loaded Models")
        table.add_column("Model")
        for m in status["loaded_models"]:
            table.add_row(m)
        console.print(table)
    else:
        console.print("[dim]No models currently loaded in vLLM[/dim]")
