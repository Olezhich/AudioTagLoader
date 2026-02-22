from pathlib import Path
import audiotagloader

import sys

if __name__ == "__main__":
    argc = len(sys.argv)

    if argc < 2:
        print(f'{sys.argv[0]}: no args')

    if argc == 4 and (sys.argv[1] == 'fetch_by_artist' or sys.argv[1] == 'fba'):
        app = audiotagloader.App(Path(sys.argv[3]).resolve())
        app.get_track_tags_by_artist(sys.argv[2])
    elif argc == 2 and (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
        print('--help, -h: run help')
        print('fetch_by_artist, fba: load audio tags by artist name and album title')
        print('\tfba "Artist name" .')
    else:
        print('try --help')



    
