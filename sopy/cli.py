import sys
from flask.cli import FlaskGroup

from sopy import create_app

cli = FlaskGroup(create_app=create_app)


def main(as_module=False):
    this_module = __package__ + '.cli'
    args = sys.argv[1:]

    if as_module:
        name = 'python -m ' + this_module.rsplit('.', 1)[0]
        sys.argv = ['-m', this_module] + sys.argv[1:]
    else:
        name = None

    cli.main(args=args, prog_name=name)


if __name__ == '__main__':
    main(as_module=True)
