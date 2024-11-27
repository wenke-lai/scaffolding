import typer

app = typer.Typer()


@app.command()
def foo():
    print("foo")


def main():
    app()
