import requests
from subprocess import DEVNULL, STDOUT, check_call, CalledProcessError
import time


hostname_to_ping = 'google.com'  # If this is down for more than 5 tests, reboot the modem.
modem_ip_address = '192.168.100.1'
modem_username = 'admin'
modem_password = 'password'


def isUp (hostname):
    try:
        response = check_call("ping -n 1 {}".format(hostname), stdout=DEVNULL, stderr=STDOUT)
    except CalledProcessError:
        response = 1

    if response == 0:
        return True
    return False

def nth(number=0):
    last_int = number % 10
    if last_int == 1:
        return 'st'
    if last_int == 2:
        return 'nd'
    if last_int == 3:
        return 'rd'
    return 'th'

def restartModem(ip_address, username, password):
    payload = {'loginUsername': username,
               'loginPassword': password,
               'resetbt': '1'}
    url = 'http://{}/goform/restore_reboot'.format(ip_address)
    if False:
        page = requests.post(url, payload)
        if 'the device is being reset' in page.text.lower():
            return True
        return False
    else:
        print('Would have rebooted modem here.')
        return True

times_not_up = 0

while True:
    if not isUp(hostname_to_ping):
        times_not_up += 1
        print("Could not ping {}.  This is the {}{} time.".format(hostname_to_ping, times_not_up, nth(times_not_up)))
    else:
        times_not_up = 0
        print("Could ping {}.  Setting times_not_up to 0".format(hostname_to_ping))

    if times_not_up >= 5:
        print("Restarting modem at {}".format(modem_ip_address))
        restartModem(modem_ip_address, modem_username, modem_password)
        i = 0
        while not isUp(modem_ip_address):
            print("{} Modem is still not up.".format(i))
            i += 1
            time.sleep(1)
        times_not_up = 0
    time.sleep(1)
