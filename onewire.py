#!/usr/bin/env python
import os
import time
import struct
import socket

# list of device id/nice name aliasses (optional)
aliasses = {
    "28BCBA7B0300004E": "cv_aanvoer",
    "2872717B03000090": "cv_retour",
    "28C7A07B030000EF": "cv_warmwater",
    "2810E8F40300003A": "meterkast",
    "2871AC7B0300007B": "vv_aanvoerbalk",
    "28B2A77B030000CD": "vv_aanvoer",
    "28C0707B03000034": "vv_retourbalk",
    "28DD8E7B03000021": "vv_retour",
    "28F7707B0300005C": "woonkamer",
    "28AF71A103000004": "zolder",
    "280B6FDB02000042": "kruipruimte",
}

base = "/sys/bus/w1/devices/"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# address for statsd server
addr = ('localhost', 8125)

while True:
    start = time.time()
    nr_devices = 0
    for device in os.listdir(base):
        id_file = os.path.join(base,device,'id')
        value_file = os.path.join(base,device,'w1_slave')
        if os.path.exists(value_file):
            device_id = file(id_file).read().encode('hex_codec').upper()
            value = float(file(value_file).readlines()[1].rsplit('t=')[-1])/1000

            name = aliasses.get(device_id, device_id)

            s = 'temps.{}:{}|ms\n'.format(name, value)
            sock.sendto(s,addr)

            nr_devices += 1

    stop = time.time() - start
    s = 'temps.runtime:%s|ms\ntemps.nr_devices:%s|g\n' % (stop, nr_devices)
    sock.sendto(s,addr)
