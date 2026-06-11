import click
from rich.table import Table
from rich.console import Console
from benchmark_cli.client import get as api_get, post as api_post

console = Console()


@click.group()
def group():
    """Task management commands"""


@group.command("list")
@click.pass_obj
def list_tasks(ctx):
    """List all evaluation tasks"""
    tasks = api_get("/tasks", ctx.url)
    table = Table(title="Evaluation Tasks")
    table.add_column("ID", width=6)
    table.add_column("Name")
    table.add_column("Dimension", width=12)
    table.add_column("Status", width=12)
    table.add_column("Created", width=20)
    status_colors = {"pending": "dim", "running": "yellow", "completed": "green", "failed": "red"}
    for t in tasks:
        color = status_colors.get(t["status"], "white")
        table.add_row(str(t["id"]), t["name"], t["dimension"], f"[{color}]{t['status']}[/{color}]", t["created_at"][:19])
    console.print(table)


@group.command("create")
@click.argument("name")
@click.option("--dimension", default="knowledge", type=click.Choice(["knowledge", "reasoning", "code", "safety"]), show_default=True)
@click.option("--models", default="", help="Comma-separated model IDs")
@click.option("--rounds", default=5, show_default=True)
@click.pass_obj
def create_task(ctx, name, dimension, models, rounds):
    """Create a new evaluation task"""
    model_ids = [int(x) for x in models.split(",") if x.strip()]
    task = api_post("/tasks", ctx.url, json={
        "name": name,
        "dimension": dimension,
        "task_type": "adversarial",
        "config": {"model_ids": model_ids, "rounds": rounds},
    })
    console.print(f"[green]Created:[/green] Task #{task['id']} '{task['name']}' ({task['dimension']})")


@group.command("start")
@click.argument("task_id", type=int)
@click.pass_obj
def start_task(ctx, task_id):
    """Start a pending evaluation task"""
    api_post(f"/tasks/{task_id}/start", ctx.url)
    console.print(f"[green]Started:[/green] Task #{task_id}")
