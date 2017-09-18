import hashlib
import os
import subprocess


BUF_SIZE = 65536


def getRegistryKey(key_path):
    try:
        x = subprocess.check_output("REG QUERY {}".format(key_path),
                                    shell=True).decode("utf-8")
        # Split on lines
        x = x.split("\r\n")
        values = {}
        i = 0
        for line in x:
            line_work = line.strip()
            if "    " in line_work:
                line_work = line_work.split("    ")
                values[line_work[0]] = {}
                values[line_work[0]]['name'] = line_work[0]
                values[line_work[0]]['type'] = line_work[1]
                values[line_work[0]]['value'] = line_work[2]
            i += 1
        return values
    except:
        return False

known_bads = ['6f7840c77f99049d788155c1351e1560b62b8ad18ad0e9adda8218b9f432f0a9',
              '1a4a5123d7b2c534cb3e3168f7032cf9ebf38b9a2a97226d0fdb7933cf6030ff',
              '36b36ee9515e0a60629d2c722b006b33e543dce1c8c2611053e0651a0bfdb2e9']

is_infected = False

# Get CCleaner install location
ccleaner = getRegistryKey('HKEY_LOCAL_MACHINE\SOFTWARE\Piriform\CCleaner')
if ccleaner:
    install_path = ccleaner['(Default)']
    for file in os.listdir(install_path['value']):
        filename = os.path.join(install_path['value'], file)
        if not os.path.isdir(filename):
            sha256 = hashlib.sha256()
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha256.update(data)
            sha_hash = sha256.hexdigest()
            status = "CLEAN"
            if sha_hash in known_bads:
                is_infected = True
                status = "INFECTED"
            print("{}: {} {}".format(file, sha_hash, status))

tcid = getRegistryKey('HKEY_LOCAL_MACHINE\SOFTWARE\Piriform\Agomo:TCID')
muid = getRegistryKey('HKEY_LOCAL_MACHINE\SOFTWARE\Piriform\Agomo:TCID')
nid = getRegistryKey('HKEY_LOCAL_MACHINE\SOFTWARE\Piriform\Agomo:TCID')

if tcid or muid or nid:
    print("Found evidence of malware being installed.")
    is_infected = True

if is_infected:
    print("Your computer shows signs of being affected.")
    print("See https://redd.it/70tnw7 for more information.")
else:
    print("Your machine seems clean.")
