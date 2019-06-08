import json
import logging
from time import sleep
from visit import visit_all_tasks

logging.getLogger().setLevel(logging.INFO)

CONFIG_FILE = "config.json"

try:
    with open(CONFIG_FILE, "r") as cf:
        config = json.load(cf)
except IOError:
    logging.error('Config file not found.')
    exit()

try:
    db_filename = config['db_file']
except KeyError:
    logging.error('DB file name not found in config.')
    exit()

try:
    notification_config = config['sendgrid']
except KeyError:
    logging.error('Sendgrid notification settings not found in config.')
    exit()

try:
    wait_time = config['wait_time']
except KeyError:
    logging.error('Waiting time not found in config.')
    exit()

try:
    with open(config['db_file'], "r") as db_file:
        db = json.load(db_file)
except IOError:
    db = {}

while True:
    visit_all_tasks(config, db)
    # update db
    with open(db_filename, "w") as db_file:
        json.dump(db, db_file, indent=4)
    logging.info('Sleeping for %d seconds...' % wait_time)
    sleep(wait_time)

