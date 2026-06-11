import click
import json
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from benchmark_cli.client import get as api_get, post as api_post

console = Console()


@click.group()
def group():
    """Report commands"""


@group.command("list")
@click.pass_obj
def list_reports(ctx):
    """List all reports"""
    reports = api_get("/reports", ctx.url)
    table = Table(title="Reports")
    table.add_column("ID", width=6)
    table.add_column("Model ID", width=10)
    table.add_column("Type", width=12)
    table.add_column("Generated", width=20)
    for r in reports:
        table.add_row(str(r["id"]), str(r["model_id"]), r.get("report_type", ""), r["generated_at"][:19])
    console.print(table)


@group.command("generate")
@click.argument("model_id", type=int)
@click.option("--type", "report_type", default="full", type=click.Choice(["full", "summary"]), show_default=True)
@click.pass_obj
def generate_report(ctx, model_id, report_type):
    """Generate a report for a model"""
    report = api_post("/reports", ctx.url, json={"model_id": model_id, "task_ids": [], "report_type": report_type})
    console.print(f"[green]Generated:[/green] Report #{report['id']} for model {model_id}")


@group.command("show")
@click.argument("report_id", type=int)
@click.pass_obj
def show_report(ctx, report_id):
    """Show report details"""
    report = api_get(f"/reports/{report_id}", ctx.url)
    content_str = json.dumps(report.get("content", {}), indent=2, ensure_ascii=False)
    console.print(Panel(content_str, title=f"Report #{report_id}", expand=False))
