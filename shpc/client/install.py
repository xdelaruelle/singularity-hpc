__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021, Vanessa Sochat"
__license__ = "MPL 2.0"


def main(args, parser, extra, subparser):

    from shpc.main import get_client

    if args.install_recipe.startswith("gh://"):
        args.container_tech = "singularity-deploy"

    cli = get_client(
        quiet=args.quiet,
        settings_file=args.settings_file,
        module=args.module,
        container_tech=args.container_tech,
    )
    cli.install(args.install_recipe)
