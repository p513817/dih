import click
import sys
import os

sys.path.append(os.path.dirname(__file__))
import handler, utils, gui

@click.group()
def main():
    gui.rich_logo()
    utils.check_docker_engine()
    pass
    # ctx.ensure_object(dict)

@main.command()
@click.option('-f', '--folder', type=str, required=True, help='Path to the folder.')
@click.option('-inc', '--includes', type=str, help='Include keys.')
@click.option('-exc', '--excludes', type=str, help='Exclude keys.')
@click.option('--debug', is_flag=True, default=False, help="Only display the information.")
@click.pass_context
def save(ctx, folder, includes, excludes, debug):
    if includes:
        includes = includes.split(',')
    if excludes:
        excludes = excludes.split(',')
    
    ids = handler.DockerSaver(
        folder=folder,
        includes=includes,
        excludes=excludes
    )
    if not debug:
        ids.start()

@main.command()
@click.option('-f', '--folder', type=click.Path(exists=True), required=True, help='Path to the folder.')
@click.option('-c', '--compose-file', type=click.Path(exists=True), help='Path to compose file.')
@click.option('-s', '--select', is_flag=True, default=False, help="Select by index.")
@click.option('--debug', is_flag=True, default=False, help="Only display the information.")
@click.pass_context
def load(ctx, folder, compose_file, select, debug):
    ids = handler.DockerLoader(
        folder=folder,
        compose_file=compose_file,
        manual=select
    )
    if not debug:
        ids.start()

if __name__ == '__main__':
    main()

