import os

from time import sleep
from collections import defaultdict
import re


def filename_to_trackname(filename):
    return filename.split('_')[1].split('.')[0]


def get_contents(path):
    return os.listdir(path)


def get_time(path):
    with open(path, errors='ignore') as f:
        raw = f.read()
    return int(int(raw.split('times best="')[1].split('"')[0]) / 10)


def ms_to_str_time(ms):
    mins = ms // 6000
    ms -= 6000 * mins
    secs = ms // 100
    ms -= 100 * secs
    return f'{str(mins).zfill(2)}:{str(secs).zfill(2)}:{str(ms).zfill(2)}'


def build_points_score(player_scores):
    _out = ''
    score_players = reversed(sorted(
        [str(player_scores[_player]).zfill(4) + ';' + _player for _player in player_scores.keys()]))
    for score_player in score_players:
        _score, _player = score_player.split(';')
        _out = _out + f' {_player}: {int(_score)}\n'
    return _out


campaign_trackname_regex = re.compile(r'[A-E]\d\d-(Race|Endurance|Obstacle|Acrobatic|Speed)')
campaign_tracks = [
    'A01-Race',
    'A02-Race',
    'A03-Race',
    'A04-Acrobatic',
    'A05-Race',
    'A06-Obstacle',
    'A07-Race',
    'A08-Endurance',
    'A09-Race',
    'A10-Acrobatic',
    'A11-Race',
    'A12-Speed',
    'A13-Race',
    'A14-Race',
    'A15-Speed',
    'B01-Race',
    'B02-Race',
    'B03-Race',
    'B04-Acrobatic',
    'B05-Race',
    'B06-Obstacle',
    'B07-Race',
    'B08-Endurance',
    'B09-Acrobatic',
    'B10-Speed',
    'B11-Race',
    'B12-Race',
    'B13-Obstacle',
    'B14-Speed',
    'B15-Race',
    'C01-Race',
    'C02-Race',
    'C03-Acrobatic',
    'C04-Race',
    'C05-Endurance',
    'C06-Speed',
    'C07-Race',
    'C08-Obstacle',
    'C09-Race',
    'C10-Acrobatic',
    'C11-Race',
    'C12-Obstacle',
    'C13-Race',
    'C14-Endurance',
    'C15-Speed',
    'D01-Endurance',
    'D02-Race',
    'D03-Acrobatic',
    'D04-Race',
    'D05-Race',
    'D06-Obstacle',
    'D07-Race',
    'D08-Speed',
    'D09-Obstacle',
    'D10-Race',
    'D11-Acrobatic',
    'D12-Speed',
    'D13-Race',
    'D14-Endurance',
    'D15-Endurance',
    'E01-Obstacle',
    'E02-Endurance',
    'E03-Endurance',
    'E04-Obstacle',
    'E05-Endurance'
]
while True:
    # Load in times
    repo_path = 'trackmaniaghosts'
    os.system(f'cd {repo_path} && git pull')
    contents = get_contents(repo_path)
    directories = filter(lambda x: '.' not in x, contents)
    tracks = defaultdict(dict)
    for player in directories:
        for replay in get_contents(f'{repo_path}//{player}'):
            tracks[filename_to_trackname(replay)][player] = get_time(f'{repo_path}//{player}/{replay}')

    # Initialise output strings
    total_player_scores = defaultdict(int)
    a_player_scores = defaultdict(int)
    b_player_scores = defaultdict(int)
    c_player_scores = defaultdict(int)
    d_player_scores = defaultdict(int)
    e_player_scores = defaultdict(int)

    time_lb = ''
    point_lb = ''

    # Build output strings
    for track in sorted(tracks.keys()):
        # Skip Non-Campaign Tracks
        if track not in campaign_tracks:
            continue

        time_players = sorted([str(tracks[track][player]).zfill(6) + ';' + player for player in tracks[track].keys()])
        best_time = int(time_players[0].split(';')[0])
        time_lb = time_lb + track + ':'
        for index, time_player in enumerate(time_players):
            time_lb = time_lb + '\n'
            time, player = time_player.split(';')
            time = int(time)
            time_diff = time - best_time
            time_lb = time_lb + f' {ms_to_str_time(time)} - {player}   +{ms_to_str_time(time_diff)}'

            score = len(time_players) - index
            total_player_scores[player] += score
            if track.startswith('A'):
                a_player_scores[player] += score
            elif track.startswith('B'):
                b_player_scores[player] += score
            elif track.startswith('C'):
                c_player_scores[player] += score
            elif track.startswith('D'):
                d_player_scores[player] += score
            elif track.startswith('E'):
                e_player_scores[player] += score

        time_lb = time_lb + '\n\n'

    point_lb = 'Total:\n' + build_points_score(total_player_scores)
    white_lb = 'White:\n' + build_points_score(a_player_scores)
    green_lb = 'Green:\n' + build_points_score(b_player_scores)
    blue_lb = 'Blue:\n' + build_points_score(c_player_scores)
    red_lb = 'Red:\n' + build_points_score(d_player_scores)
    black_lb = 'Black:\n' + build_points_score(e_player_scores)

    out = f'''
POINTS LEADERBOARD
==================
Points System: One point for finishing, plus one point per player beaten.

{point_lb}
{white_lb}
{green_lb}
{blue_lb}
{red_lb}
{black_lb}

TIME LEADERBOARD
================
{time_lb}
    '''

    out = out.replace('\n', '</br>')
    with open('/var/www/html/index.html', 'w+') as f:
        f.writelines(out)
    sleep(30)

