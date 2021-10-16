#! /usr/bin/python3

import base64
from descr import netids, mtype_to_str
from header import header, tail
import mysql.connector
import socket

mydb = mysql.connector.connect(host='mauer', user='ttnq', password='qntt', database='ttn')
c = mydb.cursor()

header()

## air time per hour ##
print('<div class="container">')
print('<h2 id="at">air time per hour</h2>')

c.execute('select h, avg(ms_airtime) as avg_ma, min(ms_airtime) as minimum, max(ms_airtime) as maximum from (select hour(time) as h, sum(size * 8 / (select bits_s from data_rates where datr_str=rxpk.datr)) as ms_airtime from rxpk group by date(time), hour(time)) as bla group by h')

print('<table><tr><th>hour</th><th>minimum</th><th>maximum</th><th>avg % of hour</th><th>avg total</th><th></th></tr>')

data = []
max_avg = -1

for (h, avg_ma, minimum, maximum) in c:
    data.append((h, avg_ma, minimum, maximum))

    if avg_ma > max_avg:
        max_avg = avg_ma

for (h, avg_ma, minimum, maximum) in data:

    stars = '&#9619;' * int(30 * (avg_ma / max_avg))

    print(f'<tr><td>{h}</td><td>{minimum:.2f}ms</td><td>{maximum:.2f}ms</td><td>{avg_ma * 100 / 3600000:.2f}%</td><td>{avg_ma:.2f}ms</td><td>{stars}</tr>')

print('</table>')

print('</div>')

tail()
