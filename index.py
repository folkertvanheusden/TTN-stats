#! /usr/bin/python3

import base64
from descr import netids, mtype_to_str
from header import header, tail
import mysql.connector
import socket

mydb = mysql.connector.connect(host='mauer', user='ttnq', password='qntt', database='ttn')
mydb2 = mysql.connector.connect(host='mauer', user='ttnq', password='qntt', database='ttn')

header()

print('<div id="toc_container">')
print('<p class="toc_title">Contents</p>')
print('<ul class="toc_list">')
print('<li><a href="#general">General data</a>')
print('<li><a href="#l10">last 10 received messages</a>')
print('<li><a href="#datr">DATR - data rate</a>')
print('<li><a href="#codr">CODR - LoRa ECC coding rate</a>')
print('<li><a href="#chan">CHAN - Receive channel</a>')
print('<li><a href="#freq">FREQ - Frequency statistics</a>')
print('<li><a href="#mtype">MTYPE - Message type</a>')
print('<li><a href="#nwkid">NWKID - Network ID</a>')
print('<li><a href="per-device.py">Statistics grouped per device</a> (new page)')
print('<li><a href="#rssi">Spreading of RSSI values</a>')
print('<li><a href="#pll">Spreading of payload lengths</a>')
print('<li><a href="#fopts">fopts frequency (how often are they repeated)</a>')
print('<li><a href="#mf">Message frequency</a>')
print('<li><a href="#at">Air time</a>')
print('<li><a href="#udev">Number of unique devices per day</a>')
print('</ul>')
print('</div>')

c = mydb.cursor()
c.execute('select count(*) as n, min(time) as first, max(time) as latest, count(distinct nwkaddr) as n_udev from rxpk')
row = c.fetchone()
n_rows = row[0]  # aprox, may change per query
first = row[1]
latest = row[2]
n_udev = row[3]

## DATR ###

print('<div class="container">')
print('<h2 id="general">General</h2>')
print('<table>')
print(f'<tr><td>total number of messages:</td><td>{n_rows}</td></tr>')
print(f'<tr><td>total number of unique devices:</td><td>{n_udev}</td></tr>')
print(f'<tr><td>first message:</td><td>{first}</td></tr>')
print(f'<tr><td>latest message:</td><td>{latest}</td></tr>')
print('</table>')
print('</div>')

## last 10 messages received ##

print('<div class="container">')
print('<h2 id="l10">last 10 messages received</h2>')

c.execute('select time, chan, freq, datr, codr, lsnr, rssi, mtype, nwkaddr, (nwkaddr >> 1) & 127 as nwkid from rxpk order by time desc limit 10')

print('<table><tr><th>time</th><th>channel</th><th>frequency</th><th>datr</th><th>codr</th><th>lsnr</th><th>rssi</th><th>mtype</th><th>nwkaddr</th><th>nwkid</th></tr>')

for (time, chan, freq, datr, codr, lsnr, rssi, mtype, nwkaddr, nwkid) in c:
    print(f'<tr><td>{time}</td><td>{chan}</td><td>{freq}MHz</td><td>{datr}</td><td>{codr}</td><td>{lsnr}dB</td><td>{rssi}dBm</td><td>{mtype_to_str(mtype)}</td><td>{nwkaddr:08x}</td><td>{netids[nwkid]}</td></tr>')

print('</table>')

print('</div>')

## DATR ###

print('<div class="container">')
print('<h2 id="datr">datr</h2>')

c = mydb.cursor()
c.execute('select datr, count(*) as n from rxpk group by datr')

print('<table><tr><th>datr</th><th>%</th><th>#</th><th></th></tr>')

for (datr, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))
    print(f'<tr><td>{datr}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## CODR ###

print('<div class="container">')
print('<h2 id="codr">codr</h2>')

c = mydb.cursor()
c.execute('select codr, count(*) as n from rxpk group by codr')

print('<table><tr><th>codr</th><th>%</th><th>#</th><th></th></tr>')

for (codr, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))
    print(f'<tr><td>{codr}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## CHAN ###

print('<div class="container">')
print('<h2 id="chan">chan</h2>')

c = mydb.cursor()
c.execute('select chan, count(*) as n from rxpk group by chan')

print('<table><tr><th>chan</th><th>%</th><th>#</th><th></th></tr>')

for (chan, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))
    print(f'<tr><td>{chan}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## frequency ###

print('<div class="container">')
print('<h2 id="freq">freq</h2>')

c = mydb.cursor()
c.execute('select freq, count(*) as n from rxpk group by freq')

print('<table><tr><th>freq</th><th>%</th><th>#</th><th></th></tr>')

for (freq, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))
    print(f'<tr><td>{freq}MHz</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## frequency ###

print('<div class="container">')
print('<h2 id="mtype">mtype</h2>')

c = mydb.cursor()
c.execute('select mtype, count(*) as n from rxpk group by mtype')

print('<table><tr><th>message type</th><th>%</th><th>#</th><th></th></tr>')

for (mtype, n) in c:
    mtype_str = mtype_to_str(mtype)

    stars = '&#9619;' * int(30 * (n / n_rows))

    print(f'<tr><td>{mtype_str}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## NWKID ###

print('<div class="container">')
print('<h2 id="nwkid">nwkid</h2>')

c = mydb.cursor()
c.execute('select (nwkaddr >> 1) & 127 as nwkid, count(*) as n from rxpk group by (nwkaddr >> 1) & 127')

data = []

for (nwkid, n) in c:
    nwkid = int(nwkid)

    if nwkid < 0:
        nwkid += 256

    data.append((nwkid, n))

data = sorted(data, key=lambda elem: elem[0])

print('<table>')

print('<tr><th>network name</th><th>nwkid</th><th>%</th><th></th></tr>')
for d in data:
    stars = '&#9619;' * int(30 * (d[1] / n_rows))

    print(f'<tr><td>{netids[d[0]]}</td><td>{d[0]:02x}</td>')
    print(f'<td title="{d[1]}">{d[1] * 100 / n_rows:.2f}</td><td>{stars}</td></tr>')

print('</table>')

print('</div>')


## RSSI ##

print('<div class="container">')
print('<h2 id="rssi">RSSI</h2>')

c = mydb.cursor()
c.execute('select max(n) as max_ from (select count(*) as n from rxpk group by floor(rssi / 5)) as i')
max_ = c.fetchone()[0]

print('<table><tr><th>RSSI</th><th></th><th>%</th><th>#</th></tr>')

c.execute('select avg(rssi) as rssi, count(*) as n from rxpk group by floor(rssi / 5)')
for (rssi, n) in c:
    stars = '&#9619;' * int(30 * (n / max_))

    print(f'<tr><td>{rssi:.02f}dBm</td><td>{stars}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td></tr>')

print('</table>')
print('</div>')

## packet lengths ##

print('<div class="container">')
print('<h2 id="pll">Payload lengths</h2>')

print('<table><tr><th>size</th><th></th><th>%</th><th>#</th></tr>')

c.execute('select avg(size) as size, count(*) as n from rxpk group by floor(size / 5)')
for (size, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))

    print(f'<tr><td>{size:.02f}B</td><td>{stars}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td></tr>')

print('</table>')
print('</div>')

## fopts ##

print('<div class="container">')
print('<h2 id="fopts">fopts (top 10)</h2>')

c = mydb.cursor()

print('<table><tr><th>fopts</th><th>%</th><th>#</th><th></th></tr>')

c.execute('select fopts, count(*) as n from rxpk group by fopts order by n desc limit 10')
for (fopts, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))

    fopts = base64.b64encode(fopts)

    print(f'<tr><td>{fopts}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## message frequency ##

print('<div class="container">')
print('<h2 id="mf">Message frequency (top 10)</h2>')

c = mydb.cursor()

print('<table><tr><th>payload</th><th>%</th><th>#</th></tr>')

c.execute('select payload, count(*) as n from rxpk group by payload order by n desc limit 10')
for (payload, n) in c:
    payload = base64.b64encode(payload)

    print(f'<tr><td>{payload}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td></tr>')

print('</table>')
print('</div>')

## air time per hour ##

print('<div class="container">')
print('<h2 id="at">air time per hour</h2>')

c.execute('select h, avg(ms_airtime) as avg_ma, min(ms_airtime) as minimum, max(ms_airtime) as maximum from (select hour(time) as h, sum(size * 8 / bits_s) as ms_airtime from rxpk, (select bits_s from rxpk, data_rates where datr_str=rxpk.datr) as rate group by date(time), hour(time)) as bla group by h')

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

## number of unique devices per day ##

print('<div class="container">')
print('<h2 id="udev">Number of unique devices per day</h2>')

c = mydb.cursor()

print('<table><tr><th>date</th><th># (count)</th></tr>')

c.execute('select d, count(*) as n from (select date(time) as d, nwkaddr from rxpk group by date(time), nwkaddr) as i group by d')
for (d, n) in c:
    print(f'<tr><td>{d}</td><td>{n}</td></tr>')

print('</table>')
print('</div>')

## number of unique devices per hour ##

print('<div class="container">')
print('<h2 id="udev">Number of unique devices per hour</h2>')

c = mydb.cursor()

print('<table><tr><th>hour</th><th># (count)</th><th></th></tr>')

c.execute('select h, count(*) from (select hour(time) as h, nwkaddr from rxpk group by hour(time), nwkaddr) as i group by h')
for (d, n) in c:
    stars = '&#9619;' * int(30 * (n / n_udev))
    print(f'<tr><td>{d}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

tail()
