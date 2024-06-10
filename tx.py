#! /usr/bin/python3

import base64
from descr import netids, mtype_to_str
from header import header, tail
import mysql.connector
import socket

mydb = mysql.connector.connect(host='localhost', user='ttnq', password='qntt', database='ttn')
mydb2 = mysql.connector.connect(host='localhost', user='ttnq', password='qntt', database='ttn')

header()

c = mydb.cursor()
c.execute('select count(*) as n, min(ts) as first, max(ts) as latest, count(distinct nwkaddr) as n_udev from txpk')
row = c.fetchone()
n_rows = row[0]  # aprox, may change per query
first = row[1]
latest = row[2]
n_udev = row[3]

## general ###

print('<div class="container">')
print('<h2 id="general">General</h2>')
print('<table>')
print(f'<tr><td>total number of messages:</td><td>{n_rows}</td></tr>')
print(f'<tr><td>total number of unique devices:</td><td>{n_udev}</td></tr>')
print(f'<tr><td>first message:</td><td>{first}</td></tr>')
print(f'<tr><td>latest message:</td><td>{latest}</td></tr>')
print('</table>')
print('</div>')

## DATR ###

print('<div class="container">')
print('<h2 id="datr">datr</h2>')

c = mydb.cursor()
c.execute('select datr, count(*) as n from txpk group by datr')

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
c.execute('select codr, count(*) as n from txpk group by codr')

print('<table><tr><th>codr</th><th>%</th><th>#</th><th></th></tr>')

for (codr, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))
    print(f'<tr><td>{codr}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## frequency ###

print('<div class="container">')
print('<h2 id="freq">freq</h2>')

c = mydb.cursor()
c.execute('select freq, count(*) as n from txpk group by freq')

print('<table><tr><th>freq</th><th>%</th><th>#</th><th></th></tr>')

for (freq, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))
    print(f'<tr><td>{freq}MHz</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## mtype ###

print('<div class="container">')
print('<h2 id="mtype">mtype</h2>')

c = mydb.cursor()
c.execute('select mtype, count(*) as n from txpk group by mtype')

print('<table><tr><th>message type</th><th>%</th><th>#</th><th></th></tr>')

for (mtype, n) in c:
    mtype_str = mtype_to_str(mtype)

    stars = '&#9619;' * int(30 * (n / n_rows))

    print(f'<tr><td>{mtype_str}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td><td>{stars}</td></tr>')

print('</table>')
print('</div>')

## packet lengths ##

print('<div class="container">')
print('<h2 id="pll">Payload lengths</h2>')

print('<table><tr><th>size</th><th></th><th>%</th><th>#</th></tr>')

c.execute('select avg(size) as size, count(*) as n from txpk group by floor(size / 5)')
for (size, n) in c:
    stars = '&#9619;' * int(30 * (n / n_rows))

    print(f'<tr><td>{size:.02f}B</td><td>{stars}</td><td>{n * 100 / n_rows:.2f}</td><td>{n}</td></tr>')

print('</table>')
print('</div>')


tail()
