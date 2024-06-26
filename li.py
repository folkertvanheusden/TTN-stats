#! /usr/bin/python3

# pip3 install mysql-connector-python

import base64
from dateutil import parser
import json
import mysql.connector
import select
import socket
import time

UDP_IP_local = '0.0.0.0'
UDP_PORT_local = 1700

UDP_IP_target = 'eu1.cloud.thethings.network'
UDP_PORT_target_local = 1701  # listening on for msgs from UDP_IP_target
UDP_PORT_target = 1700  # sending msgs to on UDP_IP_target

UDP_IP_gw = None
UDP_PORT_gw = None

sock_local = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_local.bind((UDP_IP_local, UDP_PORT_local))

sock_target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_target.bind((UDP_IP_local, UDP_PORT_target_local))

poller = select.poll()
poller.register(sock_local, select.POLLIN)
poller.register(sock_target, select.POLLIN)

mydb = mysql.connector.connect(host='127.0.0.1', user='ttn', password='ntt', database='ttn')

def make_signed_8b(v):
    if v > 127:
        return -(256 - v)

    return v

def dissect_data(data):
    if data[0] != 2:  # protocol version
        print(f"Don't know how to handle protocol version {data[0]}")
        return

    token = (data[1] << 8) | data[2]

    identifier = data[3]

    json_str = None

    if identifier == 0x00:  # PUSH_DATA
        json_str = data[12:]

        gateway_ui = data[4:12]
        gateway_ui_str = gateway_ui.hex(':')

        j = json.loads(json_str)

        if 'rxpk' in j:
            for p in j['rxpk']:
                c = mydb.cursor()

                raw = base64.b64decode(p['data'])

                mhdr = raw[0]
                mtype = mhdr >> 5       #
                rfu = (mhdr >> 2) & 7   #
                major = mhdr & 3        #

                fhdr = raw[1:]
                devaddr = fhdr[0:4]

                nwkid = devaddr[3] >> 1 #

                nwkaddr = (devaddr[0] << 24) | (devaddr[1] << 16) | (devaddr[2] << 8) | devaddr[3]

                payload = None
                fcnt = -1
                fctrl = -1
                fopts = ''
                if len(fhdr) >= 5:
                    fctrl = make_signed_8b(fhdr[4])     #
                    foptslen = fctrl & 15
                    fcnt = (fhdr[5] << 8) | fhdr[6]
                    fopts = fhdr[7:7 + foptslen]        #
                    payload = fhdr[7 + foptslen:]

                t = int(parser.parse(p['time']).timestamp())

                if 'codr' in p and 'lsnr' in p:
                    sql = 'INSERT INTO rxpk(gwui, tmst, time, tmms, chan, rfch, freq, stat, modu, datr, codr, lsnr, rssi, size, raw_data, mtype, rfu, major, nwkid, nwkaddr, fctrl, fopts, payload, fcnt) VALUES(%s, %s, FROM_UNIXTIME(%s),  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    values = [ (gateway_ui_str, p['tmst'], t, p['tmms'], p['chan'], p['rfch'], p['freq'], p['stat'], p['modu'], p['datr'], p['codr'], p['lsnr'], p['rssi'], p['size'], p['data'], mtype, rfu, major, nwkid, nwkaddr, fctrl, fopts, payload, fcnt) ]

                else:
                    sql = 'INSERT INTO rxpk(gwui, tmst, time, tmms, chan, rfch, freq, stat, modu, datr, rssi, size, raw_data, mtype, rfu, major, nwkid, nwkaddr, fctrl, fopts, payload, fcnt) VALUES(%s, %s, FROM_UNIXTIME(%s),  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    values = [ (gateway_ui_str, p['tmst'], t, p['tmms'], p['chan'], p['rfch'], p['freq'], p['stat'], p['modu'], p['datr'], p['rssi'], p['size'], p['data'], mtype, rfu, major, nwkid, nwkaddr, fctrl, fopts, payload, fcnt) ]

                c.executemany(sql, values)
                mydb.commit()


    elif identifier == 0x01:  # ACK van 0x00 (rx van hf)
        pass

    elif identifier == 0x02:  # pull data from server (soort keep-alive)0x02:  # pull data from server (soort keep-alive)
        pass

    elif identifier == 0x04:  # ack van de 0x02 pull
        pass

    elif identifier == 0x03:  # ack van de 0x04 met data om te versturen via rf
        json_str = data[4:]

        j = json.loads(json_str)

        if 'txpk' in j:
            p = j['txpk']

            c = mydb.cursor()

            raw = base64.b64decode(p['data'])

            mhdr = raw[0]
            mtype = mhdr >> 5       #
            rfu = (mhdr >> 2) & 7   #
            major = mhdr & 3        #

            fhdr = raw[1:]
            devaddr = fhdr[0:4]

            nwkid = devaddr[3] >> 1 #

            nwkaddr = (devaddr[0] << 24) | (devaddr[1] << 16) | (devaddr[2] << 8) | devaddr[3]

            # {'txpk': {'imme': False, 'tmst': 2242882236, 'freq': 867.5, 'rfch': 0, 'powe': 14, 'modu': 'LORA', 'datr': 'SF7BW125', 'codr': '4/5', 'ipol': True, 'size': 13, 'ncrc': True, 'data': 'YPdGCyaBAwAGfLIS7Q=='}}

            # create table txpk(ts datetime not null, imme int(1), tmst bigint, tmms bigint, freq double, rfch int, powe int, modu varchar(16), datr varchar(16), codr varchar(16), fdev double, ipol int(1), prea int, size int, raw_data varchar(256), ncrc int(1), mtype tinyint, nwkid tinyint, nwkaddr bigint)

            sql = 'INSERT INTO txpk(ts, imme, tmst, freq, rfch, powe, modu, datr, codr, ipol, size, raw_data, ncrc, mtype, nwkid, nwkaddr) VALUES(NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            values = [ (p['imme'], p['tmst'], p['freq'], p['rfch'], p['powe'], p['modu'], p['datr'], p['codr'], p['ipol'], p['size'], p['data'], p['ncrc'], mtype, nwkid, nwkaddr) ]

            c.executemany(sql, values)
            mydb.commit()

    elif identifier == 0x05:  # ack van de 0x03
        pass

    else:
        print(time.ctime(), identifier, data)

while True:
    fdVsEvent = poller.poll(None)

    for fd, event in fdVsEvent:
        if fd == sock_local.fileno():
            data, addr = sock_local.recvfrom(65536)
            print(addr, data)
            sock_target.sendto(data, (UDP_IP_target, UDP_PORT_target))

            UDP_IP_gw, UDP_PORT_gw = addr

            dissect_data(data)

        elif fd == sock_target.fileno():
            data, addr = sock_target.recvfrom(65536)
            print(addr, data)
            if UDP_IP_gw != None:
                sock_local.sendto(data, (UDP_IP_gw, UDP_PORT_gw))

            else:
                print('GW ip not yet known, dropping packet')

            dissect_data(data)

        else:
            print('Unknown fd; internal error', fd, sock_local, sock_target)
