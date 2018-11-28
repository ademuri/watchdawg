import urllib2
import logging
import time

def has_internet():
    try:
        urllib2.urlopen('https://google.com', timeout=5)
        return True
    except urllib2.URLError as err: 
        return False


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

while True:
    i = has_internet()
    if not i:
        logging.info('connectivity check failed, trying again')
        time.sleep(5)
        i = has_internet()

    logging.info('has internet: %d', i)
    time.sleep(60)
