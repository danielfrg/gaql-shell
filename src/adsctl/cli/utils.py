import sys
from typing import Optional

import click

from adsctl.cli.app import Application
from adsctl.config.config_file import ConfigFile
from adsctl.utils.fs import Path


def load_config(config_file_path: Optional[str] = None) -> Application:
    used_config_file = Path()
    app = Application(config_file=ConfigFile())

    if config_file_path:
        used_config_file = Path(config_file_path).resolve()
        if not used_config_file.is_file():
            click.echo(
                f"The selected config file `{str(config_file_path)}` does not exist."
            )
            sys.exit(1)
        app.config_file = ConfigFile(used_config_file)
    elif not app.config_file.path.is_file():
        click.echo("No config file found, creating one with default settings now...")

        try:
            app.config_file.restore()
            click.echo(f"Default config file created at: {app.config_file.path}")
            click.echo("Edit that file to include your Google Ads credentials.")
            sys.exit(0)
        except OSError:  # no cov
            click.echo(
                f"Unable to create config file located at `{str(app.config_file.path)}`. Please check your permissions.",
                err=True,
            )

    return app


def gaql_query(client, customer_id, query):
    ga_service = client.get_service("GoogleAdsService")
    return ga_service.search(customer_id=customer_id, query=query)


def get_first_row(response):
    for row in response:
        return row
    return None