from instapy import InstaPy
from instapy import smart_run
from account import Account
from follow import Follow
from unfollow import Unfollow
from like_by_feed import LikeByFeed
from like_by_users import LikeByUsers
from utils import key_not_exists
import random
import os
import json
import sys
import csv


if len(sys.argv) <= 1:
    sys.exit(
        '[ERROR]: Please provide the instagram account that you want to use (match with accounts.json)'
    )

account: Account = None
config: object = {}
instaname = sys.argv[1]
user_home = os.getenv('HOME')
current_user_log_path = user_home + '/InstaPy/logs/' + instaname + '/' + instaname + '_followedPool.csv'
users = []

with open(current_user_log_path, 'r') as data:
    csv_reader = csv.reader(data, delimiter='~')

    for row in csv_reader:
        users.append(row[1].strip())

with open('accounts.json', 'r') as data:
    config = json.load(data)

    if key_not_exists(instaname, config):
        sys.exit('[ERROR]: ' + instaname + ' is not exists.')
    account = Account(config[instaname])

session = InstaPy(
    username=account.get_username(),
    password=account.get_password(),
    headless_browser=False,
    multi_logs=True,
    disable_image_load=True
)

with smart_run(session):
    session.set_relationship_bounds(
        enabled=True
    )

    session.set_quota_supervisor(
        enabled=True,
        sleep_after=["likes_h", "follows_h", "unfollows_h", "server_calls_h"],
        sleepyhead=True,
        stochastic_flow=True,
        notify_me=True,
        peak_likes_hourly=57,
        peak_likes_daily=700,
        peak_follows_hourly=48,
        peak_follows_daily=None,
        peak_unfollows_hourly=35,
        peak_unfollows_daily=402,
        peak_server_calls_hourly=random.randint(150, 200),
        peak_server_calls_daily=4200
    )

    Follow(config[instaname], session)
    LikeByUsers(config[instaname], session, users)
    LikeByFeed(config[instaname], session)
    Unfollow(config[instaname], session)
