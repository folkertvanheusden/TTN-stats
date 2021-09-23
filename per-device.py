#! /usr/bin/python3

import base64
from descr import netids, mtype_to_str
from header import header, tail
import mysql.connector
import socket

mydb = mysql.connector.connect(host='mauer', user='ttnq', password='qntt', database='ttn')
mydb2 = mysql.connector.connect(host='mauer', user='ttnq', password='qntt', database='ttn')

header()

c = mydb.cursor()
c.execute('select count(*) as n, min(time) as first, max(time) as latest, count(distinct nwkaddr) as n_udev from rxpk')
row = c.fetchone()
n_rows = row[0]  # aprox, may change per query
first = row[1]
latest = row[2]
n_udev = row[3]

## per device ###

print('<div>')
print('<h2 id="perdevice">stats per device</h2>')

c = mydb.cursor()
c2 = mydb2.cursor()

c.execute('select nwkaddr, avg(rssi) as a_rssi, avg(lsnr) as a_lsnr, avg(size) as a_size, stddev(size) as sd_size, count(*) as n_msgs, (nwkaddr >> 1) & 127 as nwkid from rxpk group by nwkaddr')

idx = 0

for (nwkaddr, a_rssi, a_lsnr, a_size, sd_size, n_msgs, nwkid) in c:
    if (idx % 5) == 0:
        print('<table><tr><th>nwkaddr</th><th>avg rssi</th><th>avg lsnr</th><th>avg payload size</th><th>sd payload size</th><th># msgs</th><th>avg air time</th><th>avg # msgs/day</th></tr>')
        print('<tr><th>nwkid</th><th>first msg</th><th>last msg</th><th colspan=2>current avg total air time per day</th><th colspan=2>expected avg total air time per day</th><th title="TTN fair-use-policy">% FAP</th></tr>')

    idx += 1

    c2.execute('select avg(size * 8 / bits_s) as ms_airtime, (select count(*) / ((unix_timestamp(now()) - unix_timestamp(min(time))) / 86400) from rxpk as r where r.nwkaddr = rxpk.nwkaddr) as msgs_per_day, min(time) as first_msg, max(time) as last_msg from rxpk, (select bits_s from rxpk, data_rates where datr_str=rxpk.datr) as rate where rxpk.nwkaddr="%s" group by nwkaddr' % nwkaddr)
    row = c2.fetchone()

    msgs_per_day = row[1]
    if msgs_per_day == None and n_msgs == 1:
        msgs_per_day = 1

    adj_nwkaddr = socket.ntohl(nwkaddr)

    print(f'<tr title="{nwkaddr}" id="dev_{adj_nwkaddr}"><td>{adj_nwkaddr:08x}</td><td>{a_rssi:.02f}dBm</td><td>{a_lsnr:.02f}dB</td><td>{a_size:.02f}B</td><td>{sd_size:.02f}</td><td>{n_msgs}</td><td>{row[0]:.2f}ms</td><td>{msgs_per_day:.0f}</td></tr>')

    expected_avg_total_air_time_per_day = float(msgs_per_day * row[0])

    fap_perc = int(expected_avg_total_air_time_per_day / 30000 * 100)

    bg_color = ''
    if fap_perc > 99 and n_msgs > 1:
        bg_color = ' style="background-color:#FF4040"'

    print(f'<tr><td title="{netids[nwkid]}">{nwkid:02x}</td><td>{row[2]}</td><td>{row[3]}</td><td colspan=2>{n_msgs * row[0]:.2f}ms</td><td colspan=2>{expected_avg_total_air_time_per_day:.2f}ms</td><td{bg_color}>{fap_perc}%</td></tr>')
    print('<tr></tr>')

print('</table>')
print('</div>')

tail()
