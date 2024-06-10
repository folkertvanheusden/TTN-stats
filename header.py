#! /usr/bin/python3

def header():
    print('Content-Type: text/html')
    print('')

    print('<!DOCTYPE html>')
    print('<html>')
    print('<head>')
    print('<title>packets transmitted for TTN via LoRaWAN statistics</title>')
    print('<style>')
    print('body { font-family: Arial, Helvetica, sans-serif; border-collapse: collapse; width: 100%; }')
    print('td,th { border: 1px solid #ddd; padding: 8px; }')
    print('tr:nth-child(even){background-color: #f2f2f2;}')
    print('tr:hover {background-color: #ddd;}')
    print('th { padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #04AA6D; color: white; }')
    print('#toc_container { background: #f9f9f9 none repeat scroll 0 0; border: 1px solid #aaa; display: table; font-size: 95%; margin-bottom: 1em; padding: 20px; width: auto; }')
    print('.toc_title { font-weight: 700; text-align: center; }')
    print('#toc_container li, #toc_container ul, #toc_container ul li{ list-style: outside none none !important; }')
    print('</style>')
    print('<meta name="viewport" content="width=device-width, initial-scale=1">')
    print('<meta http-equiv="refresh" content="300"/>')
    print('</head>')
    print('<body>')

    print('<h1>packets transmitted for TTN via LoRaWAN statistics</h1>')

    print('<p><b>NOTE: AIR-TIME CALCULATION IS CURRENTLY OPTIMISTIC</b></p>')

def tail():
    print('<p><br><br></p>')

    print('<hr>')
    print('(c) 2021-2024 by Folkert van Heusden <mail@vanheusden.com>')

    print('</body>')
    print('</html>')
