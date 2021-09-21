TTN-stats
---------

This program collects all messages received from a gateway and puts that in a database.
Then, via a web-interface statistics of the received LoRa-WAN messages can be viewed.

The program (li.py) sits between the gateway software and the upstream software (e.g.
The Things Network). If the gateway supports the "Semtech UDP" json-interface, then it
should work.


li.py
-----

This script sits between the gateway and 'TTN' (or whatever LoRa-WAN network is used).

It requires "mysql-connector-python" to interface to the MySQL/MariaDB database:

    pip install mysql-connector-python

Create a database:

    create table rxpk(tmst bigint, time datetime, tmms bigint, chan int, rfch int, freq double, stat int, modu varchar(16), datr varchar(16), codr varchar(16), lsnr double, rssi double, size int, raw_data varchar(256), mtype tinyint, rfu tinyint, major tinyint, nwkid tinyint, nwkaddr bigint, fctrl tinyint, fopts blob, fcnt int, payload blob);

    CREATE TABLE `data_rates` ( `datr_str` varchar(16) NOT NULL, `bits_s` int(11) DEFAULT NULL, PRIMARY KEY (`datr_str`));
    INSERT INTO `data_rates` VALUES ('SF10BW125',980),('SF11BW125',440),('SF12BW125',250),('SF7BW125',5470),('SF7BW250',11000),('SF8BW125',3125),('SF9BW125',1760);

    grant insert,select on ttn.* to ttn@'%' identified by 'ntt'

Then point your gateway to the ip-address of where the script (li.py) is running. It uses the same port 1700.

For the "Dragino PG1301 hat' for the Raspberry Pi, this file is /etc/lora-gateway/local_conf.json


web interface
-------------

Copy the files in a directory and adjust the apache configuration:

    <Directory /var/www/htdocs/ttn>
        Options +Indexes +FollowSymLinks +MultiViews +ExecCGI
        AllowOverride None
        Order allow,deny
        allow from all
        AddHandler cgi-script .py
        DirectoryIndex index.py
    </Directory>

Adjust the mysql parameters (mysql.connector.connect()) at the top of index.py.


demo
----

https://keetweej.vanheusden.com/ttn/
