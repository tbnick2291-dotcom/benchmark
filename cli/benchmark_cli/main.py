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


from benchmark_cli.commands import model
cli.add_command(model.group, name="model")
