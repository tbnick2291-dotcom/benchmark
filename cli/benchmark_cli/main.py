import click


class Context:
    def __init__(self, url: str):
        self.url = url.rstrip("/")


@click.group()
@click.option("--url", default="http://localhost:8080", envvar="BENCHMARK_URL", show_default=True)
@click.pass_context
def cli(ctx: click.Context, url: str):
    """LLM Benchmark Platform CLI"""
    ctx.obj = Context(url)


# Commands will be added after their modules are created
# cli.add_command(model.group, name="model")
# cli.add_command(task.group, name="task")
# cli.add_command(report.group, name="report")
# cli.add_command(status.command, name="status")
