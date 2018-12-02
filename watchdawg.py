from urllib.request import urlopen
from urllib.error import URLError
import logging
import time
from datetime import datetime, timedelta
import argparse
import json

"""
INTERNET_CHECK_DELAY = 60
INTERNET_CHECK_CYCLES_TO_BAD = 10
CAN_LOAD_PAGE_RETRY_DELAY = 5
MIN_TIME_BETWEEN_REBOOTS = timedelta(hours = 1)
"""

INTERNET_CHECK_DELAY = 5
INTERNET_CHECK_CYCLES_TO_BAD = 1
CAN_LOAD_PAGE_RETRY_DELAY = 1
MIN_TIME_BETWEEN_REBOOTS = timedelta(seconds = 20)

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

parser = argparse.ArgumentParser(description='Checks for connectivity')
parser.add_argument('--file', type=str, help='file for saving hysteresis data')
# See https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
parser.add_argument('--dry_run', dest='dry_run', action='store_true', help='only log')
parser.add_argument('--nodry_run', dest='dry_run', action='store_false', help='actually perform actions')
parser.set_defaults(dry_run=True)
args = parser.parse_args()
print(args)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

last_rebooted = datetime.min
if args.file:
    try:
        with open(args.file) as f:
            saved_data = json.load(f)
            if saved_data['last_rebooted']:
                last_rebooted = datetime.strptime(saved_data['last_rebooted'], DATE_FORMAT)
                logging.info('Loaded last rebooted data: %s', last_rebooted)
    except FileNotFoundError:
        logging.info("File doesn't exist (everything is normal)") 


def can_load_page():
    try:
        urlopen('https://google.com', timeout=5)
        return True
    except URLError as err: 
        return False


def has_internet():
    i = can_load_page()
    if not i:
        logging.info('connectivity check failed, trying again')
        time.sleep(CAN_LOAD_PAGE_RETRY_DELAY)
        i = can_load_page()
    return i


no_internet_cycles = 0
while True:
    i = has_internet()
    logging.info('has internet: %d', i)
    if i:
        no_internet_cycles = 0
    else:
        no_internet_cycles += 1
        if no_internet_cycles > INTERNET_CHECK_CYCLES_TO_BAD:
            if (datetime.now() - last_rebooted) < MIN_TIME_BETWEEN_REBOOTS:
                logging.info('Would have rebooted, but rate-limited')
            else:
                no_internet_cycles = 0
                if args.dry_run:
                    logging.warning('would have rebooted')
                    last_rebooted = datetime.now()
                else:
                    logging.warning('rebooting')
                    with open(args.file, 'w') as f:
                        f.write(json.dumps({'last_rebooted': datetime.now().strftime(DATE_FORMAT)}))
                    # TODO: actually reboot

    time.sleep(INTERNET_CHECK_DELAY)
