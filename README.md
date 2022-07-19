# TrackmaniaLeaderboard
This is a very quickly and roughly thrown together leaderboard for tracking players' times recorded with [TrackmaniaGhosts](https://github.com/ScottLangridge/TrackmaniaGhosts). It's not meant to be pretty.

Quick (and very dirty) setup:
1. sudo apt update && sudo apt install apache2
1. sudo chown $USER:www-data /var/www/html -R
1. git clone git@github.com:ScottLangridge/TrackmaniaGhosts.git
1. screen
1. python3 leaderboard.py
1. ctrl + a, ctrl + d
