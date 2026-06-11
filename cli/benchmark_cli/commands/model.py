import click
from rich.table import Table
from rich.console import Console
from benchmark_cli.client import get as api_get, post as api_post, patch as api_patch

console = Console()


@click.group()
def group():
    """Model management commands"""


@group.command("list")
@click.pass_obj
def list_models(ctx):
    """List all registered models"""
    models = api_get("/models", ctx.url)
    table = Table(title="Registered Models")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Name", style="bold")
    table.add_column("Path", no_wrap=False)
    table.add_column("Status")
    for m in models:
        status_style = "green" if m["status"] == "active" else "dim"
        table.add_row(str(m["id"]), m["name"], m["model_path"], f"[{status_style}]{m['status']}[/{status_style}]")
    console.print(table)


@group.command("register")
@click.argument("name")
@click.argument("model_path")
@click.pass_obj
def register_model(ctx, name, model_path):
    """Register a new model (NAME MODEL_PATH)"""
    model = api_post("/models", ctx.url, json={"name": name, "model_path": model_path})
    console.print(f"[green]Registered:[/green] {model['name']} (id={model['id']})")


@group.command("load")
@click.argument("model_id", type=int)
@click.pass_obj
def load_model(ctx, model_id):
    """Set model status to active"""
    model = api_patch(f"/models/{model_id}/status", ctx.url, json={"status": "active"})
    console.print(f"[green]Loaded:[/green] {model['name']} → {model['status']}")


@group.command("unload")
@click.argument("model_id", type=int)
@click.pass_obj
def unload_model(ctx, model_id):
    """Set model status to inactive"""
    model = api_patch(f"/models/{model_id}/status", ctx.url, json={"status": "inactive"})
    console.print(f"[yellow]Unloaded:[/yellow] {model['name']} → {model['status']}")
