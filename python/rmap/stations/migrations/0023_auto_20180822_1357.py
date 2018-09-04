# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-22 13:57
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0022_fixture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bcode',
            name='bcode',
            field=models.CharField(default='B00000', help_text='Bcode as defined in dballe btable', max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='bcode',
            name='description',
            field=models.CharField(default='Undefined', help_text='Descriptive text', max_length=100),
        ),
        migrations.AlterField(
            model_name='bcode',
            name='unit',
            field=models.CharField(default='Undefined', help_text='Units of measure', max_length=20),
        ),
        migrations.AlterField(
            model_name='bcode',
            name='userunit',
            field=models.CharField(default='Undefined', help_text='units of measure', max_length=20),
        ),
        migrations.AlterField(
            model_name='board',
            name='category',
            field=models.CharField(choices=[('base', 'Raspberry base'), ('master', 'Mega2560 master'), ('satellite', 'Microduino core+ satellite'), ('gsm', 'Microduino core+ GSM/GPRS with GPS'), ('bluetooth', 'Microduino core+ with Bluetooth module')], max_length=50),
        ),
        migrations.AlterField(
            model_name='boardfirmwaremetadata',
            name='mac',
            field=models.CharField(blank=True, default='', help_text='MAC address', max_length=128),
        ),
        migrations.AlterField(
            model_name='boardfirmwaremetadata',
            name='swversion',
            field=models.CharField(blank=True, default='', help_text='Software version', max_length=255),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='driver',
            field=models.CharField(choices=[('I2C', 'I2C drivers'), ('RF24', 'RF24 Network jsonrpc'), ('SERI', 'SERIAL drivers over serial port'), ('JRPC', 'INDIRECT jsonrpc over some transport')], default='I2C', help_text='Driver to use', max_length=4),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='level',
            field=models.CharField(default='103,2000,-,-', help_text='Sensor metadata from rmap RFC', max_length=50),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='name',
            field=models.CharField(default='my sensor', help_text='Descriptive text', max_length=50),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='timerange',
            field=models.CharField(default='254,0,0', help_text='Sensor metadata from rmap RFC', max_length=50),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='datalevel',
            field=models.CharField(choices=[('sample', 'Sensor provide data at Level I (sample)'), ('report', 'Sensor provide data at Level II (report)')], default='sample', help_text='Data Level as defined by WMO (Sensor metadata from rmap RFC)', max_length=10),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='name',
            field=models.CharField(default='my sensor type', help_text='Descriptive text', max_length=100),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='type',
            field=models.CharField(default='TMP', help_text='Type of sensor', max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='stationconstantdata',
            name='btable',
            field=models.CharField(choices=[('B01019', 'LONG STATION OR SITE NAME                                        (CCITTIA5)'), ('B02001', 'TYPE OF STATION                                                  (CODE TABLE 2001)'), ('B02002', 'TYPE OF INSTRUMENTATION FOR WIND MEASUREMENT                     (FLAG TABLE 2002)'), ('B02003', 'TYPE OF MEASURING EQUIPMENT USED                                 (CODE TABLE 2003)'), ('B02004', 'TYPE OF INSTRUMENTATION FOR EVAPORATION MEASUREMENT OR TYPE OF C (CODE TABLE 2004)'), ('B02005', 'PRECISION OF TEMPERATURE OBSERVATION                             (K*100)'), ('B02038', 'METHOD OF WATER TEMPERATURE AND/OR SALINITY MEASUREMENT          (CODE TABLE 2038)'), ('B02039', 'METHOD OF WET-BULB TEMPERATURE MEASUREMENT                       (CODE TABLE 2039)'), ('B07030', 'HEIGHT OF STATION GROUND ABOVE MEAN SEA LEVEL (SEE NOTE 3)       (m*10)'), ('B07031', 'HEIGHT OF BAROMETER ABOVE MEAN SEA LEVEL (SEE NOTE 4)            (m*10)')], help_text='A code to define the metadata. See rmap RFC', max_length=6),
        ),
        migrations.AlterField(
            model_name='stationmetadata',
            name='category',
            field=models.CharField(choices=[('good', 'Beautifull & Good'), ('bad', 'Bad & Wrong'), ('test', 'Test & Bugs'), ('unknown', 'Unknown & Missing')], help_text='Category of the station', max_length=50),
        ),
        migrations.AlterField(
            model_name='stationmetadata',
            name='mqttmaintpath',
            field=models.CharField(default='maint', help_text='maint mqtt path for publish', max_length=100),
        ),
        migrations.AlterField(
            model_name='stationmetadata',
            name='mqttrootpath',
            field=models.CharField(default='sample', help_text='root mqtt path for publish', max_length=100),
        ),
        migrations.AlterField(
            model_name='stationmetadata',
            name='name',
            field=models.CharField(default='My station', help_text='station name', max_length=255),
        ),
        migrations.AlterField(
            model_name='stationmetadata',
            name='network',
            field=models.CharField(choices=[('fixed', 'For station with fixed coordinate'), ('mobile', 'For station with mobile coordinate')], default='fixed', help_text='station network', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportamqp',
            name='amqppassword',
            field=models.CharField(blank=True, default='', help_text='AMQP password', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportamqp',
            name='amqpserver',
            field=models.CharField(default='rmap.cc', help_text='AMQP server', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportamqp',
            name='amqpuser',
            field=models.CharField(blank=True, default='', help_text='AMQP user', max_length=9),
        ),
        migrations.AlterField(
            model_name='transportamqp',
            name='exchange',
            field=models.CharField(default='rmap', help_text='AMQP remote exchange name', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportamqp',
            name='queue',
            field=models.CharField(default='rmap', help_text='AMQP local queue name', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportmqtt',
            name='mqttpassword',
            field=models.CharField(blank=True, default='', help_text='MQTT password', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportmqtt',
            name='mqttserver',
            field=models.CharField(default='mqttserver', help_text='MQTT server', max_length=50),
        ),
        migrations.AlterField(
            model_name='transportmqtt',
            name='mqttuser',
            field=models.CharField(blank=True, default='', help_text='MQTT user', max_length=9),
        ),
        migrations.AlterField(
            model_name='transportrf24network',
            name='channel',
            field=models.PositiveIntegerField(choices=[(90, 'RF24 Network node channel 90'), (91, 'RF24 Network node channel 91'), (92, 'RF24 Network node channel 92'), (93, 'RF24 Network node channel 93'), (94, 'RF24 Network node channel 94'), (95, 'RF24 Network node channel 95')], default=93, help_text='Channel number for RF24'),
        ),
        migrations.AlterField(
            model_name='transportrf24network',
            name='iv',
            field=models.CharField(blank=True, choices=[('0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15', 'preset 1'), ('0,1,1,3,4,5,6,7,8,9,10,11,12,13,14,15', 'preset 2'), ('0,1,2,1,4,5,6,7,8,9,10,11,12,13,14,15', 'preset 3'), ('0,1,2,3,1,5,6,7,8,9,10,11,12,13,14,15', 'preset 4'), ('0,1,2,3,4,1,6,7,8,9,10,11,12,13,14,15', 'preset 5'), ('0,1,2,3,4,5,1,7,8,9,10,11,12,13,14,15', 'preset 6'), ('0,1,2,3,4,5,6,1,8,9,10,11,12,13,14,15', 'preset 7'), ('0,1,2,3,4,5,6,7,1,9,10,11,12,13,14,15', 'preset 8'), ('0,1,2,3,4,5,6,7,8,1,10,11,12,13,14,15', 'preset 9')], help_text='AES cbc iv', max_length=47, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='transportrf24network',
            name='key',
            field=models.CharField(blank=True, choices=[('0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15', 'preset 1'), ('0,1,1,3,4,5,6,7,8,9,10,11,12,13,14,15', 'preset 2'), ('0,1,2,1,4,5,6,7,8,9,10,11,12,13,14,15', 'preset 3'), ('0,1,2,3,1,5,6,7,8,9,10,11,12,13,14,15', 'preset 4'), ('0,1,2,3,4,1,6,7,8,9,10,11,12,13,14,15', 'preset 5'), ('0,1,2,3,4,5,1,7,8,9,10,11,12,13,14,15', 'preset 6'), ('0,1,2,3,4,5,6,1,8,9,10,11,12,13,14,15', 'preset 7'), ('0,1,2,3,4,5,6,7,1,9,10,11,12,13,14,15', 'preset 8'), ('0,1,2,3,4,5,6,7,8,1,10,11,12,13,14,15', 'preset 9')], help_text='AES key', max_length=47, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='transportrf24network',
            name='node',
            field=models.PositiveIntegerField(choices=[(0, 'RF24 Network node 0'), (1, 'RF24 Network node 01'), (2, 'RF24 Network node 02'), (3, 'RF24 Network node 03'), (4, 'RF24 Network node 04'), (5, 'RF24 Network node 05')], default=0, help_text='Node ID for RF24 Network'),
        ),
        migrations.AlterField(
            model_name='transportserial',
            name='baudrate',
            field=models.PositiveIntegerField(choices=[(9600, '9600'), (19200, '19200'), (38400, '38400'), (115200, '115200')], default=9600, help_text='Baud rate'),
        ),
        migrations.AlterField(
            model_name='transportserial',
            name='device',
            field=models.CharField(choices=[('COM1', 'windows COM1'), ('COM2', 'windows COM2'), ('COM3', 'windows COM3'), ('COM4', 'windows COM4'), ('COM5', 'windows COM5'), ('COM6', 'windows COM6'), ('COM7', 'windows COM7'), ('COM8', 'windows COM8'), ('COM9', 'windows COM9'), ('COM10', 'windows COM10'), ('COM11', 'windows COM11'), ('COM12', 'windows COM12'), ('COM13', 'windows COM13'), ('COM14', 'windows COM14'), ('COM15', 'windows COM15'), ('COM16', 'windows COM16'), ('COM17', 'windows COM17'), ('COM18', 'windows COM18'), ('COM19', 'windows COM19'), ('/dev/ttyUSB0', 'Linux ttyUSB0'), ('/dev/ttyUSB1', 'Linux ttyUSB1'), ('/dev/ttyUSB2', 'Linux ttyUSB2'), ('/dev/ttyUSB3', 'Linux ttyUSB3'), ('/dev/ttyUSB4', 'Linux ttyUSB4'), ('/dev/ttyACM0', 'Linux ttyACM0'), ('/dev/ttyACM1', 'Linux ttyACM1'), ('/dev/ttyACM2', 'Linux ttyACM2'), ('/dev/ttyACM3', 'Linux ttyACM3'), ('/dev/ttyACM4', 'Linux ttyACM4'), ('/dev/rfcomm0', 'Linux rfcomm0'), ('/dev/rfcomm1', 'Linux rfcomm1'), ('/dev/rfcomm2', 'Linux rfcomm2'), ('/dev/tty.HC-05-DevB', 'OSX tty.HC-05-DevB'), ('/dev/tty.usbserial', 'OSX tty.usbserial')], default='/dev/ttyUSB0', help_text='Serial device', max_length=30),
        ),
        migrations.AlterField(
            model_name='transporttcpip',
            name='name',
            field=models.CharField(choices=[('master', 'master board 1'), ('master2', 'master board 2'), ('master3', 'master board 3'), ('master4', 'master board 4'), ('stima', 'master stima 1'), ('stima2', 'master stima 2'), ('stima3', 'master stima 3'), ('stima4', 'master stima 4')], default='master', help_text='Name DSN solved (for master board only)', max_length=50),
        ),
        migrations.AlterField(
            model_name='transporttcpip',
            name='ntpserver',
            field=models.CharField(default='ntpserver', help_text='Network time server (NTP)', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='certification',
            field=models.CharField(default='ARPA-ER', max_length=20),
        ),
    ]