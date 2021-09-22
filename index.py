#! /usr/bin/python3

import base64
import mysql.connector
import socket

mydb = mysql.connector.connect(host='mauer', user='ttnq', password='qntt', database='ttn')
mydb2 = mysql.connector.connect(host='mauer', user='ttnq', password='qntt', database='ttn')

netids = [ None ] * 128
netids[0x00] = 'Private/experimental nodes'
netids[0x01] = 'Private/experimental nodes'
netids[0x02] = 'Actility'
netids[0x03] = 'Proximus'
netids[0x04] = 'Swisscom'
netids[0x05] = 'unassigned'
netids[0x06] = 'La Poste'
netids[0x07] = 'Bouygues Telecom'
netids[0x08] = 'Orbiwise'
netids[0x09] = 'SENET'
netids[0x0A] = 'KPN'
netids[0x0B] = 'EveryNet'
netids[0x0C] = 'unassigned'
netids[0x0D] = 'SK Telecom'
netids[0x0E] = 'SagemCom'
netids[0x0F] = 'Orange'
netids[0x10] = 'A2A Smart City'
netids[0x11] = 'TATA Communication'
netids[0x12] = 'Kerlink'
netids[0x13] = 'The Things Network'
netids[0x14] = 'DIGIMONDO GmbH'
netids[0x15] = 'Cisco Systems'
netids[0x16] = 'unassigned'
netids[0x17] = 'MultiTech Systems'
netids[0x18] = 'Loriot'
netids[0x19] = 'NNNCo'
netids[0x1A] = 'unassigned'
netids[0x1B] = 'TrackNet'
netids[0x1C] = 'Lar.Tech'
netids[0x1D] = 'unassigned'
netids[0x1E] = 'unassigned'
netids[0x1F] = 'Axatel  Italy'
netids[0x20] = 'Telent (Netzikon)'
netids[0x21] = 'unassigned'
netids[0x22] = 'Comcast'
netids[0x23] = 'Ventia'
netids[0x24] = 'unassigned'
netids[0x25] = 'unassigned'
netids[0x26] = 'unassigned'
netids[0x27] = 'unassigned'
netids[0x28] = 'VADSLYFE'
netids[0x29] = 'unassigned'
netids[0x2A] = 'M2B Communications'
netids[0x2B] = 'ZTE'
netids[0x2C] = 'unassigned'
netids[0x2D] = 'unassigned'
netids[0x2E] = 'unassigned'
netids[0x2F] = 'unassigned'
netids[0x30] = 'SoftBank'
netids[0x31] = 'Inmarsat'
netids[0x32] = 'Gemalto'
netids[0x33] = 'Alibaba Iot BU'
netids[0x34] = 'ER-Telecom Holding'
netids[0x35] = 'Shenzhen Tencent Computer Systems Company Limited'
netids[0x36] = 'Netze BW GmbH'
netids[0x37] = 'Tektelic'
netids[0x38] = 'Charter Communicaton'

def mtype_to_str(m):
    if mtype == 0:
        return 'join request'
    if mtype == 1:
        return 'join accept'
    if mtype == 2:
        return 'unconfirmed data up'
    if mtype == 3:
        return 'unconfirmed data down'
    if mtype == 4:
        return 'confirmed data up'
    if mtype == 5:
        return 'confirmed data down'
    if mtype == 6:
        return 'RFU'
    if mtype == 7:
        return 'proprietary'

    return '???'

print('Content-Type: text/html')
print('')

print('<!DOCTYPE html>')
print('<html>')
print('<head>')
print('<title>LoRaWAN via TTN statistics</title>')
print('<link href="stylesheet.css" rel="stylesheet" type="text/css">')
print('<meta name="viewport" content="width=device-width, initial-scale=1">')
print('<meta http-equiv="refresh" content="300"/>')
print('<link rel="icon" type="image/svg+xml" href="favicon.svg">')
print('</head>')
print('<body>')

print('<h1>LoRaWAN via TTN statistics</h1>')

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
print('<li><a href="#perdevice">Statistics grouped per device</a>')
print('<li><a href="#rssi">Spreading of RSSI values</a>')
print('<li><a href="#pll">Spreading of payload lengths</a>')
print('<li><a href="#fopts">fopts frequency (how often are they repeated)</a>')
print('<li><a href="#mf">Message frequency</a>')
print('<li><a href="#at">Air time</a>')
print('</ul>')
print('</div>')

c = mydb.cursor()
c.execute('select count(*) as n, min(time) as first, max(time) as latest from rxpk')
row = c.fetchone()
n_rows = row[0]  # aprox, may change per query
first = row[1]
latest = row[2]

## DATR ###

print('<div class="container">')
print('<h2 id="general">General</h2>')
print('<table>')
print(f'<tr><td>total number of messages:</td><td>{n_rows}</td></tr>')
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
print('<p><b>13</b>: The Things Network</p>')

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

print('<tr><th>nwkid</th><th>%</th><th></th></tr>')
for d in data:
    stars = '&#9619;' * int(30 * (d[1] / n_rows))

    print(f'<tr><td title="{netids[d[0]]}">{d[0]:02x}</td>')
    print(f'<td title="{d[1]}">{d[1] * 100 / n_rows:.2f}</td><td>{stars}</td></tr>')

print('</table>')

print('</div>')

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

c = mydb.cursor()
c.execute('select max(size) as max_size from rxpk')
max_size = c.fetchone()[0]

print('<table><tr><th>size</th><th></th><th>%</th><th>#</th></tr>')

c.execute('select avg(size) as size, count(*) as n from rxpk group by floor(size / 5)')
for (size, n) in c:
    stars = '&#9619;' * int(30 * (n / max_size))

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

print('<p><br><br></p>')

print('<hr>')
print('(c) 2021 by Folkert van Heusden <mail@vanheusden.com>')

print('</body>')
print('</html>')
