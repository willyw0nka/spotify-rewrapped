import sys
from spotify_rewrapped import SpotifyRewrapped


input_path = sys.argv[1]
output_file = sys.argv[2] + '/spotify-rewrapped.png'

SpotifyRewrapped(path=input_path, output=output_file)
