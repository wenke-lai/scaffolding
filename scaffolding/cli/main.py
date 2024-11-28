import typer

app = typer.Typer()


@app.command()
def foo():
    print("foo")


@app.command()
def bar():
    print("bar")
