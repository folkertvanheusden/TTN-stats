#! /usr/bin/python3

def header():
    print('Content-Type: text/html')
    print('')

    print('<!DOCTYPE html>')
    print('<html>')
    print('<head>')
    print('<title>TTN via LoRaWAN statistics</title>')
    print('<link href="stylesheet.css" rel="stylesheet" type="text/css">')
    print('<meta name="viewport" content="width=device-width, initial-scale=1">')
    print('<meta http-equiv="refresh" content="300"/>')
    print('<link rel="icon" type="image/svg+xml" href="favicon.svg">')
    print('</head>')
    print('<body>')

    print('<h1>TTN via LoRaWAN statistics</h1>')

    print('<p><b>NOTE: AIR-TIME CALCULATION IS CURRENTLY OPTIMISTIC</b></p>')

def tail():
    print('<p><br><br></p>')

    print('<hr>')
    print('(c) 2021 by Folkert van Heusden <mail@vanheusden.com>')

    print('</body>')
    print('</html>')
