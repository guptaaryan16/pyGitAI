import click


@click.command()
@click.option('-a', '--all', help='log all the commits generated')
def log_generated_commit(all: str)->str:
    '''Log commits that are stored and generated with AI'''
    return NotImplementedError

