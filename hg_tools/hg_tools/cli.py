"""Console script for hg_tools."""

import click

from hg_tools.commands import split, check, quality


@click.group()
def main():  # noqa
    pass


main.add_command(split)
main.add_command(check)
main.add_command(quality)


if __name__ == "__main__":
    sys.exit(main())  # noqa
