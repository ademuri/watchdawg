import urllib2
import logging
import time

INTERNET_CHECK_DELAY = 60
INTERNET_CHECK_CYCLES_TO_BAD = 10
CAN_LOAD_PAGE_RETRY_DELAY = 5

def can_load_page():
    try:
        urllib2.urlopen('https://google.com', timeout=5)
        return True
    except urllib2.URLError as err: 
        return False


def has_internet():
    i = can_load_page()
    if not i:
        logging.info('connectivity check failed, trying again')
        time.sleep(CAN_LOAD_PAGE_RETRY_DELAY)
        i = can_load_page()
    return i


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

no_internet_cycles = 0
while True:
    i = has_internet()
    logging.info('has internet: %d', i)
    if i:
        no_internet_cycles = 0
    else:
        no_internet_cycles += 1
        if no_internet_cycles > INTERNET_CHECK_CYCLES_TO_BAD:
            logging.info('would have rebooted')
            no_internet_cycles = 0

    time.sleep(INTERNET_CHECK_DELAY)
