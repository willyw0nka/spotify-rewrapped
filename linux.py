import sys
from spotify_rewrapped import SpotifyRewrapped


input_path = sys.argv[1]
output_file = sys.argv[2] + '/spotify-rewrapped.png'
timezone = sys.argv[3] if len(sys.argv) == 4 else 'UTC'

SpotifyRewrapped(path=input_path, output=output_file, timezone=timezone)
