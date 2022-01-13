import click
from spotify_rewrapped import SpotifyRewrapped

@click.command()
@click.option('--input-path', help='Input path where the StreamingHistory.json files are located.')
@click.option('--output-file', help='Output file that will be generated. Extension must be png.')
@click.option('--timezone', default='UTC', help='Timezone. You can find the full list of timezones '
              'under the TZ Database Name column https://en.wikipedia.org/wiki/List_of_tz_database_time_zones. '
              'Default is UTC.')

def main(input_path, output_file, timezone):
    click.echo(f"------------------------------------------")
    click.echo(f"Input path: {input_path}")
    click.echo(f"Output file: {output_file}")
    click.echo(f"Timezone: {timezone}")
    click.echo(f"------------------------------------------")
    SpotifyRewrapped(input_path, output_file, timezone=timezone)

if __name__ == '__main__':
    main()
